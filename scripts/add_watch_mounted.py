with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to insert the watch code - right after the fetch call
# Look for the .then part and add our watch/onMounted code

watch_code = '''
        // Watch for data changes and render charts
        watch(() => data.value, async (newData) => {
          if (newData && newData.dream_universities && newData.dream_universities.length > 0) {
            await nextTick();
            createCharts();
          }
        }, { deep: true });
        
        // Also run on mount
        onMounted(async () => {
          await nextTick();
          if (data.value && data.value.dream_universities && data.value.dream_universities.length > 0) {
            createCharts();
          }
        });
'''

# Insert after the fetch assignment
old_marker = 'const createCharts = () => {'
if old_marker in content:
    content = content.replace(
        old_marker,
        watch_code + '\n        ' + old_marker
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added watch and onMounted!')
