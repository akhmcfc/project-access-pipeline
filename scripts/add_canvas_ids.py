with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add IDs to canvas elements
content = content.replace(
    '<canvas ref=\"universitiesChart\"></canvas>',
    '<canvas id=\"universitiesChart\" ref=\"universitiesChart\"></canvas>'
)

content = content.replace(
    '<canvas ref=\"fieldsChart\"></canvas>',
    '<canvas id=\"fieldsChart\" ref=\"fieldsChart\"></canvas>'
)

content = content.replace(
    '<canvas ref=\"destinationsChart\"></canvas>',
    '<canvas id=\"destinationsChart\" ref=\"destinationsChart\"></canvas>'
)

content = content.replace(
    '<canvas ref=\"geographyChart\"></canvas>',
    '<canvas id=\"geographyChart\" ref=\"geographyChart\"></canvas>'
)

content = content.replace(
    '<canvas ref=\"schoolsChart\"></canvas>',
    '<canvas id=\"schoolsChart\" ref=\"schoolsChart\"></canvas>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added canvas IDs!')
