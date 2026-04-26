import sqlite3

conn = sqlite3.connect('students.db')
rows = conn.execute("SELECT id, email, is_admin FROM users").fetchall()
print(f"Found {len(rows)} user(s):")
for r in rows:
    print(f"  id={r[0]}  email={r[1]}  is_admin={r[2]}")
conn.close()
