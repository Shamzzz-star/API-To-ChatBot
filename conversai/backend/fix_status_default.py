"""
Fix Football-Data API default status to SCHEDULED for better results
"""
import sqlite3
import json

# Connect to database
conn = sqlite3.connect('conversai.db')
cursor = conn.cursor()

# Get Football-Data API
cursor.execute("""
    SELECT api_id, api_name, parameters 
    FROM api_registry 
    WHERE api_name LIKE '%Football%'
""")

result = cursor.fetchone()
if result:
    api_id, api_name, params_json = result
    print(f"Found API: {api_name}")
    
    # Parse current parameters
    params = json.loads(params_json)
    print(f"Current parameters: {json.dumps(params, indent=2)}")
    
    # Update status parameter default to SCHEDULED (will show upcoming and live matches)
    for param in params:
        if param['name'] == 'status':
            old_default = param.get('default_value', 'FINISHED')
            param['default_value'] = 'SCHEDULED'
            print(f"\n✅ Changed status default from '{old_default}' to 'SCHEDULED'")
            print("   This will show today's upcoming and live matches instead of only finished matches")
    
    # Update in database
    cursor.execute("""
        UPDATE api_registry 
        SET parameters = ?
        WHERE api_id = ?
    """, (json.dumps(params), api_id))
    
    conn.commit()
    print(f"\n✅ Updated {cursor.rowcount} API successfully!")
    print("\nNew parameters:")
    print(json.dumps(params, indent=2))
else:
    print("❌ Football-Data API not found")

conn.close()
