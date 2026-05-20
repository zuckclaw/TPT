#!/usr/bin/env python3
"""
True Automated TikTok Bulk Video Deleter
"""

from setup_session import setup
import time

def bulk_delete_auto():
    print("--- TikTok Automated Bulk Video Deleter ---")
    researcher = setup()
    
    if not researcher:
        print("[-] Authentication failed.")
        return

    print(f"[+] Authenticated as: {researcher.username}")
    
    # Step 1: Fetch videos automatically
    print("[*] Fetching your video list...")
    videos = researcher.get_user_videos(count=50) # Ambil 50 video terakhir
    
    if not videos:
        print("[-] No videos found or failed to fetch. Make sure your profile is not completely empty.")
        return

    print(f"\nFound {len(videos)} videos:")
    for i, vid in enumerate(videos):
        print(f"{i+1}. ID: {vid['id']} | Desc: {vid['desc'][:30]}...")

    # Step 2: Confirm deletion
    print("\n[!] WARNING: This will permanently delete the videos listed above.")
    confirm = input(f"Do you want to delete ALL {len(videos)} videos? (type 'DELETE ALL' to confirm): ")
    
    if confirm != 'DELETE ALL':
        print("[-] Operation cancelled. You must type 'DELETE ALL' exactly.")
        return

    # Step 3: Loop deletion
    print(f"\n[*] Starting automated deletion of {len(videos)} videos...")
    for i, vid in enumerate(videos):
        video_id = vid['id']
        print(f"[{i+1}/{len(videos)}] Deleting ID: {video_id} ('{vid['desc'][:20]}')...")
        
        success = researcher.delete_video(video_id)
        
        if success:
            print(f"    [+] Success.")
        else:
            print(f"    [-] Failed.")
            
        # Delay 3 detik agar tidak terlalu cepat terdeteksi sistem keamanan
        time.sleep(3)

    print("\n[+] All tasks completed.")

if __name__ == "__main__":
    bulk_delete_auto()
