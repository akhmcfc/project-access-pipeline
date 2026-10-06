with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the resetFilters function and add onMounted before the return statement
insert_before = 'const resetFilters = () => {'
onmounted_code = '''
                onMounted(() => {
                    fetchData();
                });
                
                '''

content = content.replace(
    insert_before,
    onmounted_code + insert_before
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added onMounted hook!')
