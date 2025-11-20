import sqlite3

conn = sqlite3.connect('archives.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables dans la base de données:")
for table in tables:
    print(f"- {table[0]}")

# Vérifier spécifiquement pieces_jointes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pieces_jointes'")
result = cursor.fetchone()
if result:
    print("\n✅ Table pieces_jointes existe")
else:
    print("\n❌ Table pieces_jointes n'existe pas")

conn.close() 