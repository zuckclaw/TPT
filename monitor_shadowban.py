#!/usr/bin/env python3
"""
Shadowban Real-time Monitor
"""

import requests
import json
import time
import logging
from datetime import datetime
from tiktok_research import TikTokShadowbanResearch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ShadowbanMonitor:
    def __init__(self, username, video_ids=None):
        self.researcher = TikTokShadowbanResearch(username=username)
        self.video_ids = video_ids or []
        self.history = []

    def run(self, interval_seconds=300):
        logger.info(f"Starting monitor for user: {self.researcher.username}")
        
        try:
            while True:
                timestamp = datetime.now().isoformat()
                status = self.researcher.check_shadowban_status()
                
                video_data = {}
                for vid in self.video_ids:
                    stats = self.researcher.get_video_stats(vid)
                    if stats:
                        video_data[vid] = stats

                entry = {
                    'timestamp': timestamp,
                    'status': status,
                    'videos': video_data
                }
                
                self.history.append(entry)
                self.save_history()
                
                logger.info(f"Check complete. Shadowban likely: {status['shadowban_likely']}")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user.")

    def save_history(self):
        with open(f'monitor_history_{self.researcher.username}.json', 'w') as f:
            json.dump(self.history, f, indent=2)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python monitor_shadowban.py <username> [video_id1 video_id2 ...]")
        sys.exit(1)
        
    user = sys.argv[1]
    videos = sys.argv[2:]
    
    monitor = ShadowbanMonitor(user, videos)
    monitor.run(interval_seconds=600) # Check every 10 minutes
