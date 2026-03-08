"""
Keep-Alive Script for Render Free Plan
=======================================
Run this on your PC to ping the app every 10 minutes
so it never goes to sleep.
Usage:
    python keep_alive.py
"""
import urllib.request
import time
import datetime

URL = "https://mental-health-app-chz3.onrender.com"
PING_EVERY = 10 * 60  # every 10 minutes

def ping():
    try:
        req = urllib.request.urlopen(URL, timeout=120)
        status = req.getcode()
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"  [{now}] ✅ App is awake! Status: {status}")
    except Exception as e:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"  [{now}] ⚠️  Ping failed: {e}")

print("=" * 50)
print("  🔄 Keep-Alive Script Started")
print(f"  🌍 Pinging: {URL}")
print(f"  ⏱️  Every 10 minutes")
print("  Press Ctrl+C to stop")
print("=" * 50 + "\n")

# Ping immediately on start
ping()

# Then keep pinging every 10 minutes
while True:
    time.sleep(PING_EVERY)
    ping()
