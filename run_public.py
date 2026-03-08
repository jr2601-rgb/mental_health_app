"""
Run the app publicly using ngrok.
Place ngrok.exe in the same folder as this file.

Steps:
1. Download ngrok.exe from https://ngrok.com/download
2. Place ngrok.exe in this folder
3. Run: ngrok.exe config add-authtoken YOUR_TOKEN
4. Run: python run_public.py
"""
import subprocess
import threading
import re
import sys
import os
from app import app

PORT = 5000

def start_ngrok():
    # Look for ngrok.exe in the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ngrok_path = os.path.join(script_dir, 'ngrok.exe')

    if not os.path.exists(ngrok_path):
        # Try system PATH as fallback
        ngrok_path = 'ngrok'

    print("\n" + "="*52)
    print("  🌍 Starting public tunnel via ngrok...")
    print("="*52)

    try:
        proc = subprocess.Popen(
            [ngrok_path, 'http', str(PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Give ngrok a moment to start, then fetch the public URL
        import time
        time.sleep(2)

        try:
            import urllib.request, json
            # ngrok exposes a local API to get tunnel info
            with urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels') as resp:
                data = json.loads(resp.read())
                tunnels = data.get('tunnels', [])
                for tunnel in tunnels:
                    if tunnel.get('proto') == 'https':
                        url = tunnel['public_url']
                        print("\n" + "="*52)
                        print(f"  ✅ Public URL: {url}")
                        print(f"  Share this with anyone on any network!")
                        print("  Press Ctrl+C to stop.")
                        print("="*52 + "\n")
                        return
        except Exception:
            print("  ℹ️  Tunnel started. Check http://127.0.0.1:4040 for your public URL.")

    except FileNotFoundError:
        print("\n  ❌ ngrok.exe not found!")
        print("  Download it from: https://ngrok.com/download")
        print("  Place ngrok.exe in this folder and try again.\n")
        sys.exit(1)

# Start ngrok in background
t = threading.Thread(target=start_ngrok, daemon=True)
t.start()

# Start Flask
print(f"\n  🚀 Flask running on http://localhost:{PORT}")
app.run(host='0.0.0.0', port=PORT, threaded=True, debug=False)
