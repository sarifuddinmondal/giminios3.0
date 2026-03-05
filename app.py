import sys
import threading
from flask import Flask, send_from_directory, request
import pyautogui
import os
import time
import logging
import urllib.parse
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

# ১. EXE এর ভেতর ফাইল খুঁজে পাওয়ার জন্য বিশেষ ফাংশন
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# রেসপন্স ফাস্ট করার জন্য সেটিংস
pyautogui.PAUSE = 0.001 
pyautogui.FAILSAFE = False

app = Flask(__name__)

# অপ্রয়োজনীয় লগ বন্ধ রাখা
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
    # প্রথমে index.html ওপেন হবে (লগইন/স্যামসাং বুট স্ক্রিন)
    path = resource_path('index.html')
    return send_from_directory(os.path.dirname(path), os.path.basename(path))

@app.route('/giminios')
def dashboard():
    # লগইন সফল হলে এই ড্যাশবোর্ড লোড হবে
    path = resource_path('giminios.html')
    return send_from_directory(os.path.dirname(path), os.path.basename(path))

@app.route('/remote')
def remote_page():
    path = resource_path('remote.html')
    return send_from_directory(os.path.dirname(path), os.path.basename(path))

@app.route('/tv')
def live_tv_page():
    path = resource_path('tv.html')
    return send_from_directory(os.path.dirname(path), os.path.basename(path))

@app.route('/iptv')
def iptv_manager_page():
    path = resource_path('iptv.html')
    return send_from_directory(os.path.dirname(path), os.path.basename(path))

@app.route('/launch/<app_name>')
def launch_app(app_name):
    url_map = {
        'youtube': "https://www.youtube.com/tv",
        'netflix': "https://www.netflix.com",
        'mxplayer': "http://localhost:5000/giminios",
        'hotstar': "https://www.hotstar.com",
        'jiotv': "https://www.jiotv.com",
        'ckart': "https://shop-2ca98.web.app/"
    }
    if app_name in url_map:
        window.trigger_load(url_map[app_name])
    return "Launching...", 200

@app.route('/search')
def voice_search():
    query = request.args.get('q', '')
    if query:
        window.setWindowTitle(f"GEMINI SEARCHING: {query.upper()}")
        search_url = f"https://www.youtube.com/tv#/search?search_query={urllib.parse.quote(query)}"
        window.trigger_load(search_url)
        
        def auto_play_after_search():
            time.sleep(5)
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(5)
            window.setWindowTitle("Gemini OS 3.0 Dashboard")
            
        threading.Thread(target=auto_play_after_search, daemon=True).start()
    return "Searching...", 200

@app.route('/api/<action>')
def control(action):
    try:
        window.activate_focus()
        if action == 'ok' or action == 'enter': pyautogui.press('enter')
        elif action == 'mouse_click': pyautogui.click() 
        elif action == 'play_pause': pyautogui.press('space')
        elif action == 'next_video':
            pyautogui.hotkey('ctrl', 'right') 
            time.sleep(0.4)                  
            pyautogui.press('enter')         
        elif action == 'up': pyautogui.press('up')
        elif action == 'down': pyautogui.press('down')
        elif action == 'left': pyautogui.press('left')
        elif action == 'right': pyautogui.press('right')
        elif action == 'home' or action == 'back':
            window.trigger_load("http://localhost:5000/giminios")
        elif action == 'vol_up': pyautogui.press('volumeup')
        elif action == 'vol_down': pyautogui.press('volumedown')
        elif action == 'mute': pyautogui.press('volumemute')
        elif action == 'power': QCoreApplication.quit()
        return "success", 200
    except Exception as e:
        return str(e), 500

def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)

class TVWindow(QMainWindow):
    load_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.load_signal.connect(self.load_url)
        self.browser.setFocusPolicy(Qt.StrongFocus)
        
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent("Mozilla/5.0 (WebOS; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 SmartTV")
        
        self.setCentralWidget(self.browser)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen() 
        
        self.load_url("http://localhost:5000/")
        self.setWindowTitle("Gemini OS 3.0")

    def activate_focus(self):
        self.activateWindow()
        self.raise_()
        self.browser.setFocus()

    def trigger_load(self, url):
        self.load_signal.emit(url)

    def load_url(self, url):
        self.browser.setUrl(QUrl(url))

if __name__ == '__main__':
    print("\n--- Gemini OS 3.0 Server Running ---")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    qt_app = QApplication(sys.argv)
    window = TVWindow()
    QTimer.singleShot(2000, window.activate_focus)
    sys.exit(qt_app.exec_())
