#!/usr/bin/env python3
"""
Setup Session for TikTok Shadowban Research
"""

from tiktok_research import TikTokShadowbanResearch
import json
import os

def setup():
    researcher = TikTokShadowbanResearch()

    # 1. Login via browser ke TikTok
    # 2. Buka DevTools (F12) -> Application -> Cookies
    # 3. Cari cookie: sessionid, tt_csrf_token, ds_user_id
    
    # Check if config file exists
    config_path = 'config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            cookies = json.load(f)
    else:
        print("[!] config.json not found. Please create it with your cookies.")
        cookies = {
            'sessionid': 'YOUR_SESSION_ID',
            'tt_csrf_token': 'YOUR_CSRF_TOKEN',
            'uid_tt': 'YOUR_UID_TT',
            'ttwid': 'YOUR_TTWID',
        }
        # For demonstration, we'll write a template
        with open('config_template.json', 'w') as f:
            json.dump(cookies, f, indent=4)
        print("[*] Created config_template.json. Fill it and rename to config.json")
        return None

    researcher.set_cookies(cookies)
    
    if researcher.verify_session():
        print(f"[+] Session established for: {researcher.username}")
        return researcher
    else:
        print("[-] Failed to establish session. Check your cookies.")
        return None

if __name__ == "__main__":
    setup()
