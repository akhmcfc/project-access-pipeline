with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to insert the onMounted call - right after the fetchData definition
insert_point = 'const fetchData = async () => {'

# Add onMounted call to trigger fetch on load
onmounted_code = '''
                                
                                onMounted(() => {
                                    fetchData();
                                });
                                '''

# Find the line after fetchData definition ends and insert there
if 'finally {' in content:
    # Find the closing of the finally block
    finally_close = content.rfind('} }')
    if finally_close > -1:
        content = content[:finally_close+3] + onmounted_code + content[finally_close+3:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added onMounted to trigger fetchData on load!')
