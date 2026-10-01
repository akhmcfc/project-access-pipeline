import re

with open('api/models/bootcamp_queries.py', 'r') as f:
    content = f.read()

# Replace the return statement key names
content = content.replace("'fields': fields,", "'field_distribution': fields,")
content = content.replace("'destinations': destinations,", "'destination_distribution': destinations,")

with open('api/models/bootcamp_queries.py', 'w') as f:
    f.write(content)

print('Fixed key names!')
