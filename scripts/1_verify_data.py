"""
Verify 2026 bootcamp data integrity
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config.config import BOOTCAMPERS_FILE, BOOTCAMP_YEAR

def verify_data():
    print(f"\n{'='*70}")
    print(f"VERIFYING 2026 BOOTCAMP DATA")
    print(f"{'='*70}\n")

    try:
        df = pd.read_csv(BOOTCAMPERS_FILE, encoding='utf-8')
        df = df.dropna(how='all')
        print(f"Successfully read CSV file")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False

    bootcamp_count = len(df)
    print(f"Total 2026 bootcampers: {bootcamp_count}")

    emails_present = df['Email'].notna().sum()
    print(f"Valid emails: {emails_present}/{bootcamp_count}")

    duplicates = df['Email'].duplicated().sum()
    if duplicates == 0:
        print(f"No duplicate emails")
    else:
        print(f"Found {duplicates} duplicate emails")

    print(f"\nColumns found ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")

    print(f"\nSample bootcampers:")
    for idx, row in df.head(3).iterrows():
        print(f"   {row['First name']} {row['Last Name']} ({row['Email']})")

    print(f"\n{'='*70}")
    print(f"DATA VERIFICATION COMPLETE")
    print(f"{'='*70}\n")

    return True

if __name__ == '__main__':
    verify_data()
