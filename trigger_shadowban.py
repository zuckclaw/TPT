#!/usr/bin/env python3
"""
Trigger Shadowban Scenarios - Educational Purpose Only
"""

import time
import random
import json
import logging
from tiktok_research import TikTokShadowbanResearch
from setup_session import setup

logger = logging.getLogger(__name__)

def run_experiment(researcher, video_id):
    if not researcher:
        print("[-] Researcher session not available.")
        return

    print(f"[*] Starting experiment for user: {researcher.username}")
    
    # Baseline check
    initial_status = researcher.check_shadowban_status()
    print(f"[*] Initial status: {'SHADOWBANNED' if initial_status['shadowban_likely'] else 'Normal'}")

    # Choose scenario
    print("\nSelect Scenario:")
    print("1. Rapid-fire Likes/Follows")
    print("2. Duplicate Content Simulation (Logical)")
    print("3. Banned Hashtag Simulation")
    
    choice = input("Enter choice (1-3): ")
    
    if choice == '1':
        scenario_rapid_actions(researcher)
    elif choice == '2':
        scenario_duplicate_content(researcher)
    elif choice == '3':
        scenario_banned_hashtags(researcher)
    else:
        print("Invalid choice.")
        return

    # Post-experiment monitoring
    monitor_results(researcher, video_id)

def scenario_rapid_actions(researcher):
    print("[*] Scenario 1: Rapid-fire actions...")
    count = 50
    for i in range(count):
        action = random.choice(['like', 'follow'])
        target = f"test_target_{random.randint(1000, 9999)}"
        researcher.perform_action(action, target, delay_range=(0.1, 0.5))
        
        if (i + 1) % 10 == 0:
            status = researcher.check_shadowban_status()
            print(f"    [Progress {i+1}/{count}] Status: {'SHADOWBANNED' if status['shadowban_likely'] else 'Normal'}")

def scenario_duplicate_content(researcher):
    print("[*] Scenario 2: Duplicate content simulation...")
    print("    Note: This simulates the frequency and metadata patterns of duplicate uploads.")
    for i in range(5):
        print(f"    Simulating upload #{i+1} with identical metadata...")
        time.sleep(random.uniform(5, 10))
        status = researcher.check_shadowban_status()
        print(f"    Status: {'SHADOWBANNED' if status['shadowban_likely'] else 'Normal'}")

def scenario_banned_hashtags(researcher):
    print("[*] Scenario 3: Banned hashtags...")
    banned_tags = ['adultcontent', 'gambling', 'crypto_scam'] # Examples
    for tag in banned_tags:
        print(f"    Simulating post with hashtag: #{tag}")
        time.sleep(2)
    
    time.sleep(5)
    status = researcher.check_shadowban_status()
    print(f"    Status: {'SHADOWBANNED' if status['shadowban_likely'] else 'Normal'}")

def monitor_results(researcher, video_id, duration_hours=1):
    print(f"\n[*] Starting monitoring for {duration_hours} hour(s)...")
    start_time = time.time()
    
    while time.time() - start_time < duration_hours * 3600:
        status = researcher.check_shadowban_status()
        stats = researcher.get_video_stats(video_id) if video_id else None
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'video_stats': stats
        }
        
        with open('experiment_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Views: {stats['views'] if stats else 'N/A'} | Shadowbanned: {status['shadowban_likely']}")
        
        # Wait 10 minutes between checks
        time.sleep(600)

if __name__ == "__main__":
    from datetime import datetime
    res = setup()
    if res:
        vid = input("Enter a Video ID to monitor (optional): ")
        run_experiment(res, vid if vid else None)
