/* ═══════════════════════════════════════════════════
   AI Mental Health Assessment — Global Scripts
════════════════════════════════════════════════════ */

// ── Slider live value display ──────────────────────
document.querySelectorAll('input[type=range]').forEach(slider => {
  const display = document.getElementById(slider.id + '_val');
  if (display) {
    display.textContent = slider.value;
    slider.addEventListener('input', () => display.textContent = slider.value);
  }
});

// ── Score buttons (radio-like) ─────────────────────
document.querySelectorAll('.score-group').forEach(group => {
  group.querySelectorAll('.score-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      group.querySelectorAll('.score-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      const hidden = group.parentElement.querySelector('input[type=hidden]');
      if (hidden) hidden.value = btn.dataset.value;
    });
  });
});

// ── Animated progress bar on load ─────────────────
const bar = document.getElementById('progress-bar');
if (bar) {
  const target = parseInt(bar.dataset.progress || 0);
  setTimeout(() => bar.style.width = target + '%', 200);
}

// ── GAD-7 / PHQ-9 single-question wizard ──────────
(function() {
  const steps = document.querySelectorAll('.q-step');
  if (!steps.length) return;

  let current = 0;
  const totalSteps = steps.length;
  const pBar = document.getElementById('q-progress');
  const prevBtn = document.getElementById('q-prev');
  const nextBtn = document.getElementById('q-next');
  const submitBtn = document.getElementById('q-submit');
  const counter = document.getElementById('q-counter');

  function showStep(idx) {
    steps.forEach((s, i) => {
      s.style.display = 'none';
      s.classList.remove('active');
    });
    steps[idx].style.display = 'block';
    steps[idx].classList.add('active');
    // Update dots
    document.querySelectorAll('.step-dot').forEach((d, i) => {
      d.classList.toggle('active', i === idx);
      d.classList.toggle('done', i < idx);
    });
    if (pBar) pBar.style.width = ((idx + 1) / totalSteps * 100) + '%';
    if (counter) counter.textContent = `${idx + 1} / ${totalSteps}`;
    if (prevBtn) prevBtn.style.visibility = idx === 0 ? 'hidden' : 'visible';
    if (nextBtn) nextBtn.style.display = idx < totalSteps - 1 ? 'inline-flex' : 'none';
    if (submitBtn) submitBtn.style.display = idx === totalSteps - 1 ? 'inline-flex' : 'none';
    // Fade in
    steps[idx].style.opacity = 0;
    requestAnimationFrame(() => {
      steps[idx].style.transition = 'opacity 0.4s ease';
      steps[idx].style.opacity = 1;
    });
  }

  function getAnswer(stepEl) {
    const selected = stepEl.querySelector('.score-btn.selected');
    return selected ? selected.dataset.value : null;
  }

  if (nextBtn) nextBtn.addEventListener('click', () => {
    const ans = getAnswer(steps[current]);
    if (!ans && ans !== '0') {
      steps[current].querySelector('.error-msg').style.display = 'block';
      return;
    }
    steps[current].querySelector('.error-msg').style.display = 'none';
    current++;
    showStep(current);
  });

  if (prevBtn) prevBtn.addEventListener('click', () => {
    if (current > 0) { current--; showStep(current); }
  });

  if (submitBtn) submitBtn.addEventListener('click', () => {
    const ans = getAnswer(steps[current]);
    if (!ans && ans !== '0') {
      steps[current].querySelector('.error-msg').style.display = 'block';
      return;
    }
    steps[current].querySelector('.error-msg').style.display = 'none';
    document.getElementById('q-form').submit();
  });

  showStep(0);
})();

// ── Confetti ───────────────────────────────────────
function launchConfetti() {
  const canvas = document.getElementById('confetti-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const particles = Array.from({ length: 180 }, () => ({
    x: Math.random() * canvas.width,
    y: -10,
    r: Math.random() * 8 + 4,
    d: Math.random() * 180,
    color: ['#4F46E5','#22C55E','#F59E0B','#EC4899','#06B6D4'][Math.floor(Math.random()*5)],
    tilt: Math.random() * 10 - 10,
    tiltAngle: 0,
    tiltAngleIncrementalFraction: Math.random() * 0.07 + 0.05,
  }));

  let angle = 0, tick = 0;
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    angle += 0.01;
    tick++;
    particles.forEach((p, i) => {
      p.tiltAngle += p.tiltAngleIncrementalFraction;
      p.y += (Math.cos(angle + p.d) + 3 + p.r / 2) * 0.9;
      p.x += Math.sin(angle) * 2;
      p.tilt = Math.sin(p.tiltAngle - i / 3) * 15;
      ctx.beginPath();
      ctx.lineWidth = p.r / 2;
      ctx.strokeStyle = p.color;
      ctx.moveTo(p.x + p.tilt + p.r / 4, p.y);
      ctx.lineTo(p.x + p.tilt, p.y + p.tilt + p.r / 4);
      ctx.stroke();
    });
    if (tick < 300) requestAnimationFrame(draw);
    else ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  draw();
}
if (document.getElementById('confetti-canvas')) {
  setTimeout(launchConfetti, 500);
}

// ── Animated score meter ───────────────────────────
function animateMeter(needle, score, max) {
  const pct = Math.min(score / max, 1);
  const deg = pct * 180 - 90; // -90 = left, +90 = right
  setTimeout(() => {
    needle.style.transform = `translateX(-50%) rotate(${deg}deg)`;
  }, 600);
}
document.querySelectorAll('[data-meter]').forEach(el => {
  const needle = el.querySelector('.meter-needle');
  if (needle) animateMeter(needle, +el.dataset.score, +el.dataset.max);
});

// ── Entrance stagger for suggestion cards ──────────
document.querySelectorAll('.suggestion-card').forEach((card, i) => {
  card.style.animationDelay = `${i * 0.1}s`;
});
