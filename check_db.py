import sqlite3

conn = sqlite3.connect('students.db')
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('Tables:', tables)

# Check if refresh_tokens exists
has_refresh_tokens = 'refresh_tokens' in tables
print('refresh_tokens table exists:', has_refresh_tokens)

# Check if users table has is_admin column
if 'users' in tables:
    cols = [r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
    print('Users columns:', cols)

# Check student count
if 'students' in tables:
    count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    print('Student count:', count)

# Check admission outcomes
if 'admission_outcomes' in tables:
    unalloc = conn.execute("SELECT COUNT(*) FROM admission_outcomes WHERE status='UNALLOCATED'").fetchone()[0]
    print('UNALLOCATED outcomes:', unalloc)

conn.close()
