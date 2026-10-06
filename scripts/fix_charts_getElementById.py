with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace ref-based chart creation with getElementById
content = content.replace(
    'if (universitiesChart.value && data.value.dream_universities.length > 0)',
    'const univCanvas = document.getElementById(\"universitiesChart\"); if (univCanvas && data.value.dream_universities.length > 0)'
)

content = content.replace(
    'chartInstances.universities = new Chart(universitiesChart.value,',
    'chartInstances.universities = new Chart(univCanvas,'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Switched to getElementById approach!')
