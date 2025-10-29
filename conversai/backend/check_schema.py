import sqlite3
import json

conn = sqlite3.connect('conversai.db')
cursor = conn.cursor()

# Get all columns for this API
cursor.execute('SELECT * FROM api_registry WHERE api_name LIKE "%Football%"')
row = cursor.fetchone()

# Get column names
cursor.execute('PRAGMA table_info(api_registry)')
columns = cursor.fetchall()

print("Column structure:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

print("\n" + "="*50)
print("Football-Data API Data:")
print("="*50)

if row:
    cursor.execute('SELECT api_name, endpoint, parameters FROM api_registry WHERE api_name LIKE "%Football%"')
    data = cursor.fetchone()
    print(f"\nAPI Name: {data[0]}")
    print(f"\nEndpoint: {data[1]}")
    print(f"\nParameters:")
    if data[2]:
        try:
            params = json.loads(data[2])
            print(json.dumps(params, indent=2))
        except:
            print(f"  RAW: {data[2]}")
else:
    print("NOT FOUND")

conn.close()
