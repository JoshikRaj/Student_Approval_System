import requests
import json

BASE = 'http://127.0.0.1:5000'

# Known credentials from seed_users.py
CREDENTIALS = [
    {'email': 'cm@tce.edu',    'password': 'CM@tce123',    'label': 'Primary Admin'},
    {'email': 'admin@tce.edu', 'password': 'Admin@tce123', 'label': 'Second Admin'},
    {'email': 'user1@tce.edu', 'password': 'User1@tce123', 'label': 'Staff User'},
]

print('=== 1. Testing Login ===')
token = None
for cred in CREDENTIALS:
    r = requests.post(BASE + '/api/login', json={'email': cred['email'], 'password': cred['password']})
    data = r.json()
    status_mark = 'OK' if r.status_code == 200 else 'FAIL'
    print(f"[{status_mark}] {cred['label']} ({cred['email']}) -> HTTP {r.status_code}, is_admin={data.get('is_admin')}")
    if r.status_code == 200 and not token:
        token = data['access_token']
        admin_cred = cred

if not token:
    print('\nAll logins failed! Run: python seed_users.py to create users.')
    exit(1)

label = admin_cred['label']
print(f'\nUsing token from: {label}')

print('\n=== 2. Testing GET /api/students?status=UNALLOCATED ===')
r2 = requests.get(
    BASE + '/api/students',
    params={'status': 'UNALLOCATED'},
    headers={'Authorization': 'Bearer ' + token}
)
print('HTTP Status:', r2.status_code)
d2 = r2.json()
students = d2.get('students', [])
print('Students returned:', len(students))
for s in students:
    print(f"  - [{s.get('id')}] {s.get('name')} | {s.get('application_number')} | degree={s.get('degree')}")
if not students:
    print('RAW response:', json.dumps(d2)[:500])

print('\n=== 3. Testing GET /api/statusdetails ===')
r3 = requests.get(BASE + '/api/statusdetails', headers={'Authorization': 'Bearer ' + token})
print('HTTP Status:', r3.status_code)
try:
    print('Seats data (first entry):', json.dumps(r3.json()[0] if isinstance(r3.json(), list) else r3.json())[:300])
except Exception as e:
    print('Error parsing response:', e)

print('\n=== 4. Test token refresh flow ===')
import time
print('Refresh token:', data.get('refresh_token', 'N/A')[:30], '...')
r4 = requests.post(BASE + '/api/refresh', json={'refresh_token': data.get('refresh_token')})
print('Refresh HTTP Status:', r4.status_code)
print('Refresh response:', json.dumps(r4.json())[:200])

print('\n=== ALL TESTS DONE ===')
