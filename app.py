"""
AI Mental Health Assessment System
Flask Backend — Multi-user safe, threaded
"""
from flask import Flask, render_template, request, redirect, url_for, session
from flask.sessions import SecureCookieSessionInterface
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'mental_health_secret_key_2024_xK9#mP'

# ── Increase session cookie size limit ─────────────────────────────────────
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour per session

# ── Load ML model once at startup (thread-safe read) ───────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# ─── Helper: require login ──────────────────────────────────────────────────
def require_user():
    """Returns redirect if not logged in, else None."""
    if 'user' not in session:
        return redirect(url_for('welcome'))
    return None

# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def welcome():
    # Already logged in — go to dashboard
    if 'user' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if len(username) < 2:
            error = 'Please enter a name with at least 2 characters.'
        else:
            session.clear()               # clean slate for new user
            session['user'] = username
            session.permanent = True      # respect PERMANENT_SESSION_LIFETIME
            return redirect(url_for('dashboard'))
    return render_template('welcome.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome'))

@app.route('/dashboard')
def dashboard():
    guard = require_user()
    if guard: return guard
    return render_template('dashboard.html', username=session['user'])

@app.route('/basic-questions', methods=['GET', 'POST'])
def basic_questions():
    guard = require_user()
    if guard: return guard
    if request.method == 'POST':
        # Store only what we need — keep cookie small
        session['basic'] = {
            'age':               int(request.form.get('age', 25)),
            'gender':            int(request.form.get('gender', 0)),
            'sleep_hours':       float(request.form.get('sleep_hours', 7)),
            'work_hours':        float(request.form.get('work_hours', 8)),
            'physical_activity': int(request.form.get('physical_activity', 3)),
            'social_interaction':int(request.form.get('social_interaction', 5)),
            'stress_level':      int(request.form.get('stress_level', 5)),
            'screen_time':       float(request.form.get('screen_time', 4)),
            'caffeine':          int(request.form.get('caffeine', 2)),
            'alcohol':           int(request.form.get('alcohol', 1)),
            'family_history':    int(request.form.get('family_history', 0)),
            'therapy_history':   int(request.form.get('therapy_history', 0)),
        }
        session.modified = True
        return redirect(url_for('anxiety'))
    return render_template('basic_questions.html')

@app.route('/anxiety', methods=['GET', 'POST'])
def anxiety():
    guard = require_user()
    if guard: return guard
    if request.method == 'POST':
        answers = [int(request.form.get(f'q{i}', 0)) for i in range(1, 8)]
        session['anxiety_score'] = sum(answers)   # just store the score, not all answers
        session.modified = True
        return redirect(url_for('depression'))
    return render_template('anxiety.html')

@app.route('/depression', methods=['GET', 'POST'])
def depression():
    guard = require_user()
    if guard: return guard
    if request.method == 'POST':
        answers = [int(request.form.get(f'q{i}', 0)) for i in range(1, 10)]
        session['depression_score'] = sum(answers)
        session.modified = True
        return redirect(url_for('result'))
    return render_template('depression.html')

@app.route('/result')
def result():
    guard = require_user()
    if guard: return guard

    basic            = session.get('basic', {})
    anxiety_score    = session.get('anxiety_score', 0)
    depression_score = session.get('depression_score', 0)

    features = pd.DataFrame([{
        'age':               basic.get('age', 25),
        'gender':            basic.get('gender', 0),
        'sleep_hours':       basic.get('sleep_hours', 7),
        'work_hours':        basic.get('work_hours', 8),
        'physical_activity': basic.get('physical_activity', 3),
        'social_interaction':basic.get('social_interaction', 5),
        'stress_level':      basic.get('stress_level', 5),
        'screen_time':       basic.get('screen_time', 4),
        'caffeine':          basic.get('caffeine', 2),
        'alcohol':           basic.get('alcohol', 1),
        'family_history':    basic.get('family_history', 0),
        'therapy_history':   basic.get('therapy_history', 0),
        'anxiety_score':     anxiety_score,
        'depression_score':  depression_score,
    }])

    prediction = int(model.predict(features)[0])
    proba      = model.predict_proba(features)[0].tolist()

    labels = {0: 'Healthy', 1: 'Moderate Risk', 2: 'High Risk'}
    colors = {0: 'healthy', 1: 'moderate',      2: 'high'}

    if   anxiety_score <= 4:  anxiety_level = 'Minimal'
    elif anxiety_score <= 9:  anxiety_level = 'Mild'
    elif anxiety_score <= 14: anxiety_level = 'Moderate'
    else:                     anxiety_level = 'Severe'

    if   depression_score <= 4:  depression_level = 'Minimal'
    elif depression_score <= 9:  depression_level = 'Mild'
    elif depression_score <= 14: depression_level = 'Moderate'
    elif depression_score <= 19: depression_level = 'Moderately Severe'
    else:                        depression_level = 'Severe'

    return render_template('result.html',
        username         = session['user'],
        prediction       = prediction,
        prediction_label = labels[prediction],
        prediction_color = colors[prediction],
        anxiety_score    = anxiety_score,
        anxiety_level    = anxiety_level,
        depression_score = depression_score,
        depression_level = depression_level,
        suggestions      = get_suggestions(prediction),
        proba            = proba,
        basic            = basic,
    )

@app.route('/ending')
def ending():
    guard = require_user()
    if guard: return guard
    return render_template('ending.html', username=session['user'])

@app.route('/restart')
def restart():
    session.clear()                      # wipe everything — name, scores, answers
    return redirect(url_for('welcome'))  # back to name entry page


# ─── Suggestions ────────────────────────────────────────────────────────────

def get_suggestions(prediction):
    base = [
        {"icon": "🧘", "title": "Mindfulness & Meditation",
         "desc": "Practice 10 minutes of daily mindfulness to reduce stress and improve focus."},
        {"icon": "🏃", "title": "Regular Exercise",
         "desc": "Aim for 30 minutes of physical activity at least 3–5 days per week."},
        {"icon": "😴", "title": "Sleep Hygiene",
         "desc": "Maintain a consistent sleep schedule of 7–9 hours per night."},
        {"icon": "🥗", "title": "Balanced Nutrition",
         "desc": "Eat a balanced diet rich in whole foods and stay well hydrated."},
    ]
    if prediction >= 1:
        base += [
            {"icon": "💬", "title": "Talk to Someone",
             "desc": "Share your feelings with a trusted friend, family member, or counselor."},
            {"icon": "📵", "title": "Reduce Screen Time",
             "desc": "Limit screen exposure, especially before bedtime."},
        ]
    if prediction == 2:
        base += [
            {"icon": "🩺", "title": "Seek Professional Help",
             "desc": "Consider speaking with a licensed mental health professional or therapist."},
            {"icon": "📞", "title": "Crisis Support",
             "desc": "If in distress, contact a mental health helpline in your region immediately."},
        ]
    return base


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True,
    )
