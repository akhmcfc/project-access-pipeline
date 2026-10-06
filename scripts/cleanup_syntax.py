with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove any orphaned onMounted calls
content = content.replace('onMounted(() => {', '')
content = content.replace('fetchData();', '')
content = content.replace('});', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Cleaned up syntax errors!')
