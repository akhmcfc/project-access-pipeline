# Add routes to public_routes.py

# Read the file
with open('api/routes/public_routes.py', 'r') as f:
    content = f.read()

# Find where to insert (before the last line or before if __name__)
insertion_point = content.rfind('@bp.route')
if insertion_point != -1:
    # Find the end of the last route function
    next_def = content.find('\n@', insertion_point + 1)
    if next_def == -1:
        next_def = len(content) - 100
    
    new_routes = '''

@bp.route('/geographic-distribution', methods=['GET'])
def geographic_distribution():
    data = get_geographic_distribution()
    return jsonify({"count": len(data), "cities": data})

@bp.route('/schools', methods=['GET'])
def schools_distribution():
    data = get_schools_distribution()
    return jsonify({"count": len(data), "schools": data})
'''
    
    content = content[:next_def] + new_routes + content[next_def:]
    
    with open('api/routes/public_routes.py', 'w') as f:
        f.write(content)
    
    print('Added routes!')
else:
    print('Could not find insertion point')
