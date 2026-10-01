import sys

with open('api/routes/public_routes.py', 'r') as f:
    lines = f.readlines()

# Find and remove the broken import lines (11-14)
new_lines = []
skip_count = 0
for i, line in enumerate(lines):
    if i == 9:  # Line 10 (0-indexed)
        new_lines.append('from api.models.bootcamp_queries import get_dashboard_data, get_dream_universities, get_field_distribution, get_destination_distribution, get_geographic_distribution, get_schools_distribution, get_bootcamp_count, get_survey_1_summary, get_survey_2_summary, get_survey_3_summary\n')
        skip_count = 4  # Skip the next 4 broken lines
    elif skip_count > 0:
        skip_count -= 1
    else:
        new_lines.append(line)

with open('api/routes/public_routes.py', 'w') as f:
    f.writelines(new_lines)

print('Fixed imports!')
