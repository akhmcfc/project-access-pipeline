with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add missing closing brace for data.ref
content = content.replace(
    '''schools: []
                
                
                const chartInstances''',
    '''schools: []
                });
                
                const chartInstances'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed missing closing brace for data.ref!')
