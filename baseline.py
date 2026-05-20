#!/usr/bin/env python3
"""
Baseline Metrics Recorder
"""

import json
from datetime import datetime
from tiktok_research import TikTokShadowbanResearch
from setup_session import setup

def record_baseline():
    print("[*] Recording baseline metrics...")
    researcher = setup()
    
    if not researcher:
        # If no session, at least try public metrics
        username = input("Enter username to check baseline (publicly): ")
        researcher = TikTokShadowbanResearch(username=username)
    else:
        username = researcher.username

    video_id = input("Enter a Video ID for baseline monitoring: ")
    
    baseline = {
        'timestamp': datetime.now().isoformat(),
        'username': username,
        'video_id': video_id,
        'metrics': researcher.get_video_stats(video_id) if video_id else None,
        'status': researcher.check_shadowban_status(username)
    }

    print(f"\n[BASELINE] Data:\n{json.dumps(baseline, indent=2)}")

    filename = f'baseline_{username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w') as f:
        json.dump(baseline, f, indent=2)
    print(f"[*] Baseline saved to {filename}")

if __name__ == "__main__":
    record_baseline()
