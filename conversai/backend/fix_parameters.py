"""
Fix Football-Data API - make status optional with default
"""
import sqlite3
import json

conn = sqlite3.connect('conversai.db')
cursor = conn.cursor()

# Update parameters to make status optional with default
new_parameters = {
    "required": [],
    "optional": [
        {
            "name": "status",
            "type": "string",
            "description": "Match status (SCHEDULED, LIVE, FINISHED)",
            "default": "FINISHED"
        },
        {
            "name": "competitions",
            "type": "string",
            "description": "Competition code (PL=Premier League, PD=La Liga, SA=Serie A, BL1=Bundesliga, FL1=Ligue 1)"
        },
        {
            "name": "date",
            "type": "string",
            "description": "Date in YYYY-MM-DD format"
        }
    ]
}

cursor.execute('''
    UPDATE api_registry 
    SET parameters = ? 
    WHERE api_name LIKE '%Football%'
''', (json.dumps(new_parameters),))

if cursor.rowcount > 0:
    print(f"✅ Updated parameters for Football-Data API")
    print(f"\n📝 New configuration:")
    print(f"   - status: OPTIONAL (default: FINISHED)")
    print(f"   - competitions: OPTIONAL")
    print(f"   - date: OPTIONAL (auto-filled)")
else:
    print("❌ No API found")

conn.commit()
conn.close()

print("\n✨ Done! The API should work now.")
