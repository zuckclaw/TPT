#!/usr/bin/env python3
"""
Analyze Shadowban Research Results
"""

import json
import matplotlib.pyplot as plt
from datetime import datetime

def analyze_log(file_path):
    print(f"[*] Analyzing log: {file_path}")
    
    data = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
    except FileNotFoundError:
        print(f"[-] File {file_path} not found.")
        return

    if not data:
        print("[-] No data to analyze.")
        return

    timestamps = [datetime.fromisoformat(d['timestamp']) for d in data]
    
    # Check if we have video stats
    has_video_stats = any(d.get('video_stats') for d in data)
    
    if has_video_stats:
        views = [d['video_stats']['views'] if d['video_stats'] else 0 for d in data]
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, views, marker='o', label='Views')
        plt.title('Video Views Over Time')
        plt.xlabel('Time')
        plt.ylabel('Views')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('analysis_views.png')
        print("[+] Generated analysis_views.png")

    # Analyze Shadowban status
    sb_status = [1 if d['status']['shadowban_likely'] else 0 for d in data]
    plt.figure(figsize=(10, 2))
    plt.step(timestamps, sb_status, where='post', color='red')
    plt.title('Shadowban Status (1=Likely, 0=Normal)')
    plt.yticks([0, 1])
    plt.ylim(-0.5, 1.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('analysis_shadowban.png')
    print("[+] Generated analysis_shadowban.png")

    # Summary
    total_checks = len(data)
    sb_count = sum(sb_status)
    print(f"\n[SUMMARY]")
    print(f"Total checks: {total_checks}")
    print(f"Shadowban detected in: {sb_count} checks ({(sb_count/total_checks)*100:.1f}%)")
    
    if has_video_stats:
        start_views = views[0]
        end_views = views[-1]
        growth = end_views - start_views
        print(f"Total view growth: {growth}")

if __name__ == "__main__":
    import sys
    log_file = sys.argv[1] if len(sys.argv) > 1 else 'experiment_log.json'
    analyze_log(log_file)
