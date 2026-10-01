"""
4b_clean_data.py - Data Cleaning & Normalization
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import pandas as pd
import json
from datetime import datetime
from config.config import DATABASE_FILE

UNCERTAIN_KEYWORDS = [
    'probably', 'maybe', 'perhaps', 'possibly',
    'might', 'could', 'unsure', 'uncertain',
    'still exploring', 'not sure', 'thinking about',
    'considering', 'possibly interested', 'leaning towards'
]

SEPARATORS = [',', ';', ' or ', ' / ', ' and ']

FIELD_MAPPINGS = {
    'Law': 'Law',
    'Business': 'Business & Economics',
    'Medicine': 'Medicine & Health Sciences',
    'Engineering': 'STEM',
    'CS': 'STEM',
    'Computer Science': 'STEM',
    'Physics': 'STEM',
    'Math': 'STEM',
    'Social Sciences': 'Social Sciences',
    'Humanities': 'Humanities',
    'Arts': 'Arts & Design'
}

def flag_uncertainty(text):
    """Check if text contains uncertain language"""
    if not text or pd.isna(text):
        return False, None
    
    text_lower = str(text).lower()
    found_keywords = []
    
    for keyword in UNCERTAIN_KEYWORDS:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return len(found_keywords) > 0, found_keywords

def split_multi_value(text, field_type='general'):
    """Split comma/semicolon-separated values"""
    if not text or pd.isna(text):
        return []
    
    text = str(text).strip()
    values = []
    remaining = text
    
    for sep in SEPARATORS:
        if sep in remaining:
            remaining = remaining.replace(sep, '|')
    
    values = [v.strip() for v in remaining.split('|') if v.strip()]
    return values

def normalize_field_value(value, field_type):
    """Normalize field values to standard categories"""
    if not value or pd.isna(value):
        return None
    
    value = str(value).strip()
    
    if field_type == 'field_of_study':
        for key, mapped in FIELD_MAPPINGS.items():
            if key.lower() in value.lower():
                return mapped
    
    return value

def clean_dream_universities(text):
    """Clean university field - split multi-values"""
    values = split_multi_value(text)
    cleaned = []
    for v in values:
        v = v.replace('(UK)', '').replace('(USA)', '').replace('(Switzerland)', '').strip()
        if v:
            cleaned.append(v)
    return cleaned

def clean_field_of_study(text):
    """Clean field of study - normalize to standard categories"""
    values = split_multi_value(text)
    cleaned = []
    for v in values:
        normalized = normalize_field_value(v, 'field_of_study')
        if normalized:
            cleaned.append(normalized)
    return cleaned

def generate_quality_report(results):
    """Generate data quality metrics"""
    total = len(results)
    report = {
        'total_records': total,
        'records_with_uncertainty': sum(1 for r in results if r['is_uncertain']),
        'records_with_multi_values': sum(1 for r in results if r['multi_value_count'] > 1),
        'avg_multi_values': sum(r['multi_value_count'] for r in results) / total if total > 0 else 0,
        'uncertainty_fields': {}
    }
    
    for field in ['dream_universities', 'field_of_study', 'target_destinations']:
        uncertain_in_field = sum(1 for r in results if r.get(f'{field}_uncertain', False))
        report['uncertainty_fields'][field] = uncertain_in_field
    
    return report

def clean_data():
    """Main data cleaning pipeline"""
    print("\n" + "="*70)
    print("🧹 CLEANING SURVEY 1 DATA (2026 Bootcampers)")
    print("="*70 + "\n")
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT candidate_id, dream_universities, target_destinations, field_of_study
        FROM pre_bootcamp_2026
    ''')
    
    records = cursor.fetchall()
    conn.close()
    
    cleaned_results = []
    
    for candidate_id, dream_unis, destinations, field_of_study in records:
        is_uncertain, uncertain_keywords = flag_uncertainty(
            f"{dream_unis} {destinations} {field_of_study}"
        )
        
        cleaned_unis = clean_dream_universities(dream_unis)
        cleaned_fields = clean_field_of_study(field_of_study)
        
        result = {
            'candidate_id': candidate_id,
            'original_dream_universities': dream_unis,
            'cleaned_dream_universities': cleaned_unis,
            'university_count': len(cleaned_unis),
            'original_field_of_study': field_of_study,
            'cleaned_field_of_study': cleaned_fields,
            'field_count': len(cleaned_fields),
            'target_destinations': destinations,
            'is_uncertain': is_uncertain,
            'uncertain_keywords': uncertain_keywords,
            'multi_value_count': len(cleaned_unis) + len(cleaned_fields),
            'data_quality_score': 1.0 if not is_uncertain else 0.7
        }
        
        cleaned_results.append(result)
        print(f"✅ {candidate_id}")
        if is_uncertain:
            print(f"   ⚠️  Uncertain language: {uncertain_keywords}")
        if len(cleaned_unis) > 1:
            print(f"   📚 Multiple universities: {cleaned_unis}")
        if len(cleaned_fields) > 1:
            print(f"   🎓 Multiple fields: {cleaned_fields}")
    
    quality_report = generate_quality_report(cleaned_results)
    
    print(f"\n{'='*70}")
    print("📊 DATA QUALITY REPORT")
    print(f"{'='*70}")
    print(f"Total records: {quality_report['total_records']}")
    print(f"Records with uncertain language: {quality_report['records_with_uncertainty']} ({quality_report['records_with_uncertainty']/quality_report['total_records']*100:.1f}%)")
    print(f"Records with multiple values: {quality_report['records_with_multi_values']}")
    print(f"Avg values per record: {quality_report['avg_multi_values']:.1f}")
    print(f"\nUncertainty by field:")
    for field, count in quality_report['uncertainty_fields'].items():
        print(f"  - {field}: {count} records")
    
    df_cleaned = pd.DataFrame(cleaned_results)
    df_cleaned.to_csv('data/processed/2026_cleaned_survey1.csv', index=False)
    
    with open('data/processed/2026_data_quality_report.json', 'w') as f:
        json.dump(quality_report, f, indent=2)
    
    save_cleaning_rules()
    
    print(f"\n{'='*70}")
    print("✅ CLEANING COMPLETE")
    print(f"{'='*70}")
    print(f"📄 Cleaned data: data/processed/2026_cleaned_survey1.csv")
    print(f"📊 Quality report: data/processed/2026_data_quality_report.json")
    print(f"📋 Cleaning rules: docs/DATA_CLEANING_RULES.md")

def save_cleaning_rules():
    """Save cleaning rules for reuse on 2023-2025 data"""
    rules = """# Data Cleaning Rules (Reusable for 2023-2025)

## Overview
These rules developed during 2026 data cleaning.

## Rule 1: Uncertain Language Flagging
Flag but keep original text containing uncertain language.

## Rule 2: Multi-Value Splitting
Split comma/semicolon-separated values into individual entries.

## Rule 3: Field of Study Normalization
Map similar fields to standard categories.

## Rule 4: University Name Cleanup
Remove country codes, trim whitespace.
"""
    
    with open('docs/DATA_CLEANING_RULES.md', 'w') as f:
        f.write(rules)

if __name__ == '__main__':
    clean_data()
