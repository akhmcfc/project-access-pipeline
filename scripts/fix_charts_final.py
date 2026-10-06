with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add IDs to all canvas elements
replacements = [
    ('<canvas ref=\"universitiesChart\"></canvas>', '<canvas id=\"universitiesChart\"></canvas>'),
    ('<canvas ref=\"fieldsChart\"></canvas>', '<canvas id=\"fieldsChart\"></canvas>'),
    ('<canvas ref=\"destinationsChart\"></canvas>', '<canvas id=\"destinationsChart\"></canvas>'),
    ('<canvas ref=\"geographyChart\"></canvas>', '<canvas id=\"geographyChart\"></canvas>'),
    ('<canvas ref=\"schoolsChart\"></canvas>', '<canvas id=\"schoolsChart\"></canvas>'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added canvas IDs!')
