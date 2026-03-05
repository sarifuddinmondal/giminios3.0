import sys
import threading
import pyautogui
import os
import time
import logging
import urllib.parse
from flask import Flask, send_from_directory, request
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from supabase import create_client, Client

# ১. সুপাবেস কনফিগারেশন
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ২. EXE রিসোর্স পাথ ফাংশন
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pyautogui.PAUSE = 0.001 
pyautogui.FAILSAFE = False
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# --- ক্লাউড লিসেনার ---
def cloud_command_listener():
    print("Cloud Sync: Online (Waiting for commands...)")
    last_processed_id = None
    while True:
        try:
            response = supabase.table("remote_commands").select("*").order("created_at", desc=True).limit(1).execute()
            if response.data:
                latest_data = response.data[0]
                current_id = latest_data['id']
                command = latest_data['command']
                if current_id != last_processed_id:
                    last_processed_id = current_id
                    print(f"Action Received: {command}")
                    process_action(command)
            time.sleep(0.4)
        except Exception as e:
            print(f"Syncing Error: {e}")
            time.sleep(2)

def process_action(action):
    try:
        window.activate_focus()
        if action.isdigit(): pyautogui.press(action)
        elif action == 'ok' or action == 'enter': pyautogui.press('enter')
        elif action == 'up': pyautogui.press('up')
        elif action == 'down': pyautogui.press('down')
        elif action == 'left': pyautogui.press('left')
        elif action == 'right': pyautogui.press('right')
        elif action == 'back': pyautogui.press('backspace')
        elif action == 'play_pause': pyautogui.press('space')
        elif action == 'vol_up': pyautogui.press('volumeup')
        elif action == 'vol_down': pyautogui.press('volumedown')
        
        # অ্যাপ নেভিগেশন
        elif action == 'home':
            window.trigger_load("https://yourusername.github.io/your-repo/index.html")
        elif action == 'launch_yt':
            window.trigger_load("https://www.youtube.com/tv")
        
        # নতুন যোগ করা IPTV লজিক
        elif action == 'iptv':
            # আপনার দেওয়া লিঙ্কটি এখানে ইন্টিগ্রেট করা হয়েছে
            target_url = "https://iptv-org.github.io/iptv/countries/in.m3u"
            # আপনি যদি চান এটি আপনার নিজস্ব iptv.html এ ওপেন হোক, তবে সেটি সেট করুন:
            window.trigger_load(f"https://yourusername.github.io/your-repo/iptv.html?url={target_url}")

        elif action.startswith('search:'):
            query = action.split(':')[1]
            search_url = f"https://www.youtube.com/tv#/search?search_query={urllib.parse.quote(query)}"
            window.trigger_load(search_url)

    except Exception as e:
        print(f"PyAutoGUI Error: {e}")

# --- PyQt5 Window ---
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
        self.load_url("https://yourusername.github.io/your-repo/index.html")

    def activate_focus(self):
        self.activateWindow()
        self.raise_()
        self.browser.setFocus()

    def trigger_load(self, url):
        self.load_signal.emit(url)

    def load_url(self, url):
        self.browser.setUrl(QUrl(url))

if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    window = TVWindow() # Global window instance
    threading.Thread(target=cloud_command_listener, daemon=True).start()
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False), daemon=True).start()
    QTimer.singleShot(2000, window.activate_focus)
    sys.exit(qt_app.exec_())
