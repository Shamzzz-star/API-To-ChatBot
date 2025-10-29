"""
Quick script to fix Football-Data API keywords
"""
import sqlite3
import json

# Connect to database
conn = sqlite3.connect('conversai.db')
cursor = conn.cursor()

# New keywords that will match better
new_keywords = [
    "score",
    "scores", 
    "football",
    "soccer",
    "match",
    "matches",
    "live",
    "fixture",
    "fixtures",
    "result",
    "results",
    "league",
    "premier",
    "yesterday"
]

# Update the Football-Data API
cursor.execute('''
    UPDATE api_registry 
    SET intent_keywords = ? 
    WHERE api_name LIKE '%Football%'
''', (json.dumps(new_keywords),))

# Check if update was successful
if cursor.rowcount > 0:
    print(f"✅ Updated {cursor.rowcount} API(s)")
    
    # Verify the update
    cursor.execute("SELECT api_name, intent_keywords FROM api_registry WHERE api_name LIKE '%Football%'")
    result = cursor.fetchone()
    if result:
        print(f"\n📝 API Name: {result[0]}")
        print(f"🔑 New Keywords: {json.loads(result[1])}")
else:
    print("❌ No API found matching 'Football'")

# Commit changes
conn.commit()
conn.close()

print("\n✨ Done! Try your query again.")
