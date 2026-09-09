# Project Access Finland - Bootcamp Analytics Pipeline

## Overview
Automated three-stage survey pipeline to track bootcamper journey:
- **Survey 1 (Pre-bootcamp):** Baseline aspirations
- **Survey 2 (Mid-bootcamp):** Progress & changes  
- **Survey 3 (Post-bootcamp):** Outcomes & impact

## Scope
**Pipeline tracks:** Bootcampers only (85-90 in 2026)
**Context data:** All applicants (400+) for demographic comparison

## Quick Start

`ash
# 1. Verify data
python scripts/1_verify_data.py

# 2. Setup database
python scripts/2_setup_database.py

# 3. Generate candidate IDs
python scripts/3_generate_candidate_ids.py

# 4. Load data
python scripts/4_load_data.py

# 5. Generate survey links
python scripts/5_generate_typeform_links.py
`

## Project Structure
- /data — Raw & processed data
- /database — SQLite database
- /scripts — Pipeline scripts
- /surveys — Typeform configurations
- /docs — Documentation
