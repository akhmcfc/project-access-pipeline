"""
9_scheduled_sync.py - Automatically sync Typeform responses daily
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import schedule
import time
from scripts.ingest_typeform_responses import ingest_all_responses
def sync_job():
    """Daily sync job"""
    print(f"\n{'='*70}")
    print(f"🔄 STARTING SCHEDULED SYNC")
    print(f"{'='*70}\n")
    ingest_all_responses()
    print(f"\n✅ Sync complete at {time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")

def start_scheduler():
    """Start the scheduler - runs daily at 8 AM UTC"""
    schedule.every().day.at("08:00").do(sync_job)
    
    print("\n" + "="*70)
    print("📅 SCHEDULED SYNC STARTED")
    print("="*70)
    print("Syncing daily at 08:00 UTC")
    print("Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == '__main__':
    start_scheduler()
