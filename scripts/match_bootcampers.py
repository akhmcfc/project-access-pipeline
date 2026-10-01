import pandas as pd
import re

# Load files
bootcampers_df = pd.read_csv('data/processed/2026_candidate_ids.csv')
applicants_df = pd.read_csv('data/raw/PA_Fin_2026_Bootcamp_Applications.csv')

print('Matching bootcampers with applicants...\n')

matched_data = []
unmatched = []

for idx, bootcamper in bootcampers_df.iterrows():
    bootcamper_email = bootcamper['email'].lower().strip()
    
    # Find matching applicant by Email (uppercase E)
    matching = applicants_df[
        applicants_df['Email'].str.lower().str.strip() == bootcamper_email
    ]
    
    if len(matching) == 0:
        unmatched.append(bootcamper_email)
        print(f"  WARNING: {bootcamper['first_name']}: NOT FOUND")
    else:
        applicant = matching.iloc[0]
        uni_col = 'Milloin todennäköisesti alottaisit yliopistossa? 📅'
        uni_year = applicant[uni_col]
        
        # Parse year from '*2027* syksy' -> 2027
        match = re.search(r'(20\d{2})', str(uni_year))
        year = int(match.group(1)) if match else None
        
        matched_data.append({
            'candidate_id': bootcamper['candidate_id'],
            'email': bootcamper_email,
            'first_name': bootcamper['first_name'],
            'last_name': bootcamper['last_name'],
            'uni_start_year': year
        })
        
        print(f"  OK: {bootcamper['first_name']} -> {year}")

# Summary
print(f'\nMatched: {len(matched_data)}/{len(bootcampers_df)}')
if unmatched:
    print(f'Unmatched: {len(unmatched)}')

# Show breakdown by year
results = pd.DataFrame(matched_data)
print('\nBootcampers by start year:')
print(results['uni_start_year'].value_counts().sort_index())

# Save
results.to_csv('data/processed/2026_bootcampers_with_uni_years.csv', index=False)
print('\nSaved to: data/processed/2026_bootcampers_with_uni_years.csv')
print('\nPreview:')
print(results[['candidate_id', 'first_name', 'uni_start_year']].head(10))
