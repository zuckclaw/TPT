#!/usr/bin/env python3
"""
TikTok Shadowban Research Tool - Educational Purpose Only
Memonitor dan menganalisis shadowban dengan mensimulasikan perilaku
"""

import requests
import time
import random
import json
import logging
from datetime import datetime
from urllib.parse import quote

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TikTokShadowbanResearch:
    """
    Tool riset untuk memahami shadowban TikTok.
    Mencatat perubahan reach, impressions, dan FYP performance.
    """
    
    def __init__(self, username=None):
        self.session = requests.Session()
        self.username = username
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.tiktok.com/',
            'Origin': 'https://www.tiktok.com',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }
        self.action_log = []
        
    def set_cookies(self, cookies_dict):
        """Set session cookies from a logged-in session"""
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies_dict)
        logger.info("Cookies set successfully.")
    
    def verify_session(self):
        """Verify if the session is valid using a more reliable account info endpoint"""
        # Endpoint alternatif yang sering lebih stabil untuk cek sesi
        url = "https://www.tiktok.com/passport/web/account/info/"
        
        headers = self.base_headers.copy()
        # TikTok sering mengecek tt-csrf-token di header untuk request API
        csrf_token = self.session.cookies.get('tt_csrf_token')
        if csrf_token:
            headers['tt-csrf-token'] = csrf_token
            
        try:
            resp = self.session.get(url, headers=headers)
            logger.info(f"Verification request sent. Status: {resp.status_code}")
            
            if resp.ok:
                try:
                    data = resp.json()
                    # Passport API returns { "message": "success", "data": { ... } }
                    if data.get('message') == 'success' or data.get('data', {}).get('user_id'):
                        user_data = data.get('data', {})
                        self.username = user_data.get('username') or user_data.get('unique_id')
                        logger.info(f"Session verified! Logged in as: {self.username}")
                        return True
                    else:
                        logger.warning(f"Session seems invalid or expired. API Response: {data}")
                except ValueError:
                    logger.error("Response is not JSON. TikTok might be blocking the request or showing a CAPTCHA.")
                    # Print a bit of the response to see what it is (HTML, etc)
                    snippet = resp.text[:200].replace('\n', ' ')
                    logger.error(f"Response snippet: {snippet}")
            else:
                logger.error(f"HTTP Error {resp.status_code}")
                if resp.status_code == 403:
                    logger.error("403 Forbidden: IP atau User-Agent Anda mungkin diblokir sementara.")
            
            return False
        except Exception as e:
            logger.error(f"Exception during verification: {e}")
            return False

    def get_user_videos(self, count=30):
        """Fetch a list of video IDs from the user's own profile"""
        # Note: TikTok uses different endpoints for this, but this is a common one for web
        url = f"https://www.tiktok.com/api/post/item_list/?uniqueId={self.username}&count={count}"
        
        headers = self.base_headers.copy()
        try:
            resp = self.session.get(url, headers=headers)
            if resp.ok:
                data = resp.json()
                items = data.get('itemList', [])
                video_list = []
                for item in items:
                    video_list.append({
                        'id': item.get('id'),
                        'desc': item.get('desc', 'No description'),
                        'create_time': item.get('createTime')
                    })
                return video_list
            else:
                logger.error(f"Failed to fetch videos: {resp.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error fetching videos: {e}")
            return []

    def delete_video(self, video_id):
        """Delete a video from the user's profile"""
        url = "https://www.tiktok.com/api/item/delete/"
        
        headers = self.base_headers.copy()
        csrf_token = self.session.cookies.get('tt_csrf_token')
        if csrf_token:
            headers['tt-csrf-token'] = csrf_token
            
        params = {
            'itemId': video_id,
            'device_id': self.session.cookies.get('device_id', '7300000000000000000'),
        }
        
        try:
            # TikTok deletion usually requires a POST request
            resp = self.session.post(url, headers=headers, params=params)
            if resp.ok:
                data = resp.json()
                if data.get('status_code') == 0 or data.get('message') == 'success':
                    logger.info(f"Video {video_id} deleted successfully.")
                    return True
                else:
                    logger.error(f"Failed to delete video: {data}")
            else:
                logger.error(f"HTTP Error during deletion: {resp.status_code}")
            return False
        except Exception as e:
            logger.error(f"Exception during deletion: {e}")
            return False

    def get_video_stats(self, video_id):
        """Get public video stats for monitoring"""
        url = f"https://www.tiktok.com/api/item/detail/?itemId={video_id}"
        try:
            resp = self.session.get(url, headers=self.base_headers)
            if resp.ok:
                data = resp.json()
                item_struct = data.get('itemInfo', {}).get('itemStruct', {})
                if not item_struct:
                    logger.warning(f"No item structure found for video {video_id}")
                    return None
                
                stats = item_struct.get('stats', {})
                return {
                    'video_id': video_id,
                    'timestamp': datetime.now().isoformat(),
                    'views': stats.get('playCount', 0),
                    'likes': stats.get('diggCount', 0),
                    'shares': stats.get('shareCount', 0),
                    'comments': stats.get('commentCount', 0),
                    'collects': stats.get('collectCount', 0),
                }
            logger.error(f"Failed to get video stats: {resp.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error getting video stats: {e}")
            return None
    
    def perform_action(self, action_type, target, delay_range=(2, 5)):
        """
        Simulasi aksi pengguna untuk trigger analysis
        
        action_type: 'like', 'follow', 'comment', 'view'
        """
        time.sleep(random.uniform(*delay_range))
        
        logger.info(f"Performing {action_type} on {target}")
        
        # In a real tool, this would call TikTok internal APIs
        # For this research tool, we log it and simulate the effect
        self.action_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action_type,
            'target': target
        })
        
        return True
    
    def rapid_actions_sequence(self, count=50):
        """
        Simulasi aktivitas tidak wajar (bot-like)
        untuk memicu shadowban detection
        """
        logger.warning(f"Starting rapid action sequence ({count} actions)...")
        
        for i in range(count):
            if i % 10 == 0:
                logger.info(f"Progress: {i}/{count}")
            
            action = random.choice(['like', 'follow', 'view'])
            target = f"user_{random.randint(10000, 99999)}"
            
            self.perform_action(action, target, delay_range=(0.1, 0.3))
            
    def check_shadowban_status(self, username=None):
        """
        Memeriksa indikator shadowban:
        1. Search visibility
        2. Hashtag visibility (simulated)
        """
        target_username = username or self.username
        if not target_username:
            logger.error("No username provided for shadowban check.")
            return None

        results = {
            'timestamp': datetime.now().isoformat(),
            'username': target_username,
            'search_visible': False,
            'shadowban_likely': False
        }
        
        # Test: Search user by username
        search_url = f"https://www.tiktok.com/api/search/general/?keyword={quote(target_username)}"
        try:
            resp = self.session.get(search_url, headers=self.base_headers)
            if resp.ok:
                data = resp.json()
                users = data.get('data', [])
                for item in users:
                    if item.get('type') == 1: # User type
                        u = item.get('user', {})
                        if u.get('uniqueId', '').lower() == target_username.lower():
                            results['search_visible'] = True
                            break
            else:
                logger.error(f"Search API failed: {resp.status_code}")
        except Exception as e:
            logger.error(f"Error during search visibility check: {e}")

        results['shadowban_likely'] = not results['search_visible']
        return results

if __name__ == "__main__":
    # Example usage
    researcher = TikTokShadowbanResearch()
    print("TikTok Shadowban Research Tool Loaded.")
