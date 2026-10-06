with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add console.log to createCharts
old_create = 'const createCharts = () => {'
new_create = '''const createCharts = () => {
                    console.log('createCharts called', data.value.dream_universities);'''

content = content.replace(old_create, new_create)

# Add logging to fetchData completion
old_fetch = 'setTimeout(() => {'
new_fetch = '''console.log('Data loaded:', data.value);
                        setTimeout(() => {'''

content = content.replace(old_fetch, new_fetch)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added debug logging!')
