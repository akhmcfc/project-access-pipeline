with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the broken onMounted call (line 700 area)
content = content.replace(
    '''onMounted(() => {
                    fetchData();
                });''',
    ''
)

# Also remove any orphaned onMounted lines
lines = content.split('\n')
cleaned_lines = [line for line in lines if 'onMounted(() => {' not in line or 'fetchData();' not in line]
content = '\n'.join(cleaned_lines)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Removed broken onMounted code!')
