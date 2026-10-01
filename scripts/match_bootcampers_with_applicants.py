import pandas as pd
import os

# ============================================================
# STEP 1: Load the 36 selected bootcampers
# ============================================================

bootcamper_file = 'data/processed/2026_candidate_ids.csv'

print("Loading 36 selected bootcampers...")
bootcampers_df = pd.read_csv(bootcamper_file)

print(f"Loaded {len(bootcampers_df)} bootcampers")

# ============================================================
# STEP 2: Load all 234 applicants
# ============================================================

applicants_file = 'data/raw/PA_Fin_2026_Bootcamp_Applications.csv'

print(f"Loading 234 applicants...")
applicants_df = pd.read_csv(applicants_file)

print(f"Loaded {len(applicants_df)} applicants")

# ============================================================
# STEP 3: Match bootcampers with applicants by email
# ============================================================

print("\nMatching bootcampers with applicants by email...")

matched_data = []
unmatched_bootcampers = []

for idx, bootcamper in bootcampers_df.iterrows():
    bootcamper_email = bootcamper['email'].lower().strip()
    
    # Find matching applicant by email
    matching_applicants = applicants_df[
        applicants_df['email'].str.lower().str.strip() == bootcamper_email
    ]
    
    if len(matching_applicants) == 0:
        unmatched_bootcampers.append(bootcamper_email)
        print(f"  ⚠️  {bootcamper['first_name']} ({bootcamper_email}): NOT FOUND")
        
    else:
        applicant = matching_applicants.iloc[0]
        
        # Extract university start year column
        uni_start_column = 'Milloin todennäköisesti alottaisit yliopistossa? 📅'
        uni_start_year = applicant[uni_start_column]
        
        matched_data.append({
            'candidate_id': bootcamper['candidate_id'],
            'email': bootcamper_email,
            'first_name': bootcamper['first_name'],
            'last_name': bootcamper['last_name'],
            'expected_uni_start_year': uni_start_year
        })
        
        print(f"  ✓ {bootcamper['first_name']} → {uni_start_year}")

# ============================================================
# STEP 4: Create results DataFrame
# ============================================================

results_df = pd.DataFrame(matched_data)

print(f"\n✓ Successfully matched {len(matched_data)}/{len(bootcampers_df)} bootcampers")

if unmatched_bootcampers:
    print(f"❌ {len(unmatched_bootcampers)} bootcampers NOT found")

# ============================================================
# STEP 5: Parse university start year
# ============================================================

print("\nParsing university start years...")

def parse_uni_year(year_string):
    """Extract year from strings like '*2028* syksy'"""
    if pd.isna(year_string):
        return None
    
    year_str = str(year_string).strip()
    
    import re
    match = re.search(r'(20\d{2})', year_str)
    if match:
        return int(match.group(1))
    
    return None

results_df['uni_start_year_parsed'] = results_df['expected_uni_start_year'].apply(parse_uni_year)

# ============================================================
# STEP 6: Summary by year
# ============================================================

print("\nBootcampers by expected university start year:")
year_counts = results_df['uni_start_year_parsed'].value_counts().sort_index()
for year, count in year_counts.items():
    print(f"  {year}: {count} bootcampers")

# ============================================================
# STEP 7: Save the matched data
# ============================================================

output_file = 'data/processed/2026_bootcampers_with_uni_years.csv'
results_df.to_csv(output_file, index=False)

print(f"\n✓ Saved to {output_file}")
print("\nPreview:")
print(results_df[['candidate_id', 'first_name', 'uni_start_year_parsed']].head(10))