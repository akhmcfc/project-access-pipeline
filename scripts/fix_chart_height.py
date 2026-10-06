with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add height to chart containers
content = content.replace(
    '<div class="chart-wrapper">',
    '<div class="chart-wrapper" style="height: 400px;">'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added chart heights!')
