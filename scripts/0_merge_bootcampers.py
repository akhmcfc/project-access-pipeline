"""
Filter to x-confirmed bootcampers only, merge with full application data.
Includes manual email overrides for known mismatches.
Fixes UTF-8 encoding to preserve Finnish characters correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config.config import DATA_DIR

CONFIRMED_LIST = os.path.join(DATA_DIR, 'raw', 'PA_2026_confirmed_list.csv')
FULL_APPLICATIONS = os.path.join(DATA_DIR, 'raw', 'PA_Fin_2026_Bootcamp_Applications.csv')
OUTPUT_FILE = os.path.join(DATA_DIR, 'processed', 'PA_2026_bootcampers_final.csv')

EMAIL_OVERRIDES = {
    'nika.dettmann@gmail.com': 'nika.dettmann@icloud.com',
    'pinja.liski1@gmail.com': 'pinja.liski@icloud.com',
}

def merge_bootcampers():
    print(f"\n{'='*70}")
    print(f"FILTERING CONFIRMED BOOTCAMPERS")
    print(f"{'='*70}\n")

    confirmed = pd.read_csv(CONFIRMED_LIST, sep='\t', encoding='utf-8')
    confirmed.columns = confirmed.columns.str.strip()
    confirmed['Email'] = confirmed['Email'].astype(str).str.strip().str.lower()

    x_only = confirmed[confirmed['Confirmation'].astype(str).str.strip() == 'x'].copy()
    print(f"Total in confirmation list: {len(confirmed)}")
    print(f"Confirmed with x: {len(x_only)}")

    dupes = x_only['Email'].duplicated().sum()
    if dupes > 0:
        print(f"WARNING: {dupes} duplicate emails among confirmed - dropping repeats")
        x_only = x_only.drop_duplicates(subset='Email', keep='first')

    override_count = 0
    for confirmed_email, real_email in EMAIL_OVERRIDES.items():
        mask = x_only['Email'] == confirmed_email
        if mask.any():
            x_only.loc[mask, 'Email'] = real_email
            override_count += mask.sum()
    if override_count > 0:
        print(f"Applied {override_count} manual email override(s)")

    applications = pd.read_csv(FULL_APPLICATIONS, encoding='utf-8')
    applications = applications.dropna(how='all')
    applications['Email'] = applications['Email'].astype(str).str.strip().str.lower()
    applications = applications.drop_duplicates(subset='Email', keep='last')

    # Drop the redundant name columns from applications - we already have
    # First name / Last Name from the confirmed list, no need to duplicate.
    applications = applications.drop(columns=['First name', 'Last name'], errors='ignore')

    merged = x_only[['First name', 'Last Name', 'Email']].merge(
        applications, on='Email', how='left'
    )

    data_col = merged.columns[3] if len(merged.columns) > 3 else None
    matched = merged[data_col].notna().sum() if data_col else 0
    print(f"\nMatched against full application data: {matched}/{len(merged)}")

    if data_col:
        unmatched = merged[merged[data_col].isna()]
        if len(unmatched) > 0:
            print(f"WARNING: These confirmed bootcampers had no match in the application file:")
            for _, row in unmatched.iterrows():
                print(f"   {row['First name']} {row['Last Name']} - {row['Email']}")

    os.makedirs(os.path.join(DATA_DIR, 'processed'), exist_ok=True)
    merged.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')

    print(f"\n{'='*70}")
    print(f"FINAL BOOTCAMPER COUNT: {len(merged)}")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    merge_bootcampers()
