import sqlite3
import json

conn = sqlite3.connect('conversai.db')
cursor = conn.cursor()

cursor.execute('SELECT api_name, parameters, endpoint FROM api_registry WHERE api_name LIKE "%Football%"')
row = cursor.fetchone()

if row:
    print(f"API Name: {row[0]}")
    print(f"\nEndpoint: {row[1]}")
    print(f"\nParameters:")
    params = json.loads(row[2])
    print(json.dumps(params, indent=2))
else:
    print("NOT FOUND")

conn.close()
