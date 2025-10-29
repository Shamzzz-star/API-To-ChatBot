"""
Final fix for Football-Data API:
1. Remove default status value (allow all match statuses)
2. Make date parameter truly optional (no default)
This allows team-based queries to return latest matches regardless of date/status
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
    print(f"\nCurrent parameters: {json.dumps(params, indent=2)}")
    
    # Update parameters:
    # 1. Remove default value from status (allow all statuses)
    # 2. Ensure date has no default (already should be optional)
    
    # Handle both required and optional parameters
    for param_type in ['required', 'optional']:
        if param_type in params and isinstance(params[param_type], list):
            for param in params[param_type]:
                if isinstance(param, dict):
                    if param.get('name') == 'status':
                        if 'default' in param or 'default_value' in param:
                            old_default = param.get('default') or param.get('default_value')
                            param.pop('default', None)
                            param.pop('default_value', None)
                            print(f"\n✅ Removed status default value (was: '{old_default}')")
                            print("   Now API will return all match statuses (SCHEDULED, LIVE, FINISHED)")
                    
                    if param.get('name') == 'date':
                        param.pop('default', None)
                        param.pop('default_value', None)
                        print(f"\n✅ Date parameter has no default - will return latest matches when not specified")
    
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
    
    print("\n" + "="*60)
    print("CHANGES SUMMARY:")
    print("="*60)
    print("✅ Status parameter: No default (returns all match statuses)")
    print("✅ Date parameter: No default (returns latest matches)")
    print("\nNow queries like 'Manchester United match' will:")
    print("  - Return latest Manchester United matches")
    print("  - Include SCHEDULED, LIVE, and FINISHED matches")
    print("  - Not be limited to a specific date")
    print("="*60)
else:
    print("❌ Football-Data API not found")

conn.close()
