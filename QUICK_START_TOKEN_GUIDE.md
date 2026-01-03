### 🔐 QUICK START - TOKEN AUTHENTICATION GUIDE

```
STEP 1: Login Request (NO AUTH NEEDED)
═════════════════════════════════════════════════════════════════
POST http://127.0.0.1:8000/api/v1/auth/login/
Content-Type: application/json

{
  "email": "rutuja@gmail.com",
  "password": "rutu12345"
}

⬇️ SERVER RESPONSE (Copy the token!) ⬇️

{
  "auth_token": "9944b09199c62bcf9418ad846dd0e4bbea6f7f7f",  ← COPY THIS!
  "user_id": 1,
  "email": "rutuja@gmail.com",
  "first_name": "Rutuja",
  "last_name": "Kumar",
  "role": "student",
  "message": "Login successful"
}


STEP 2: Use Token in Requests (FOR ALL OTHER APIs)
═════════════════════════════════════════════════════════════════
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6f7f7f

Example:
GET http://127.0.0.1:8000/api/v1/students/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6f7f7f


STEP 3: VS Code REST Client - Token Variable
═════════════════════════════════════════════════════════════════
In test.http file, you can use:

@token = 9944b09199c62bcf9418ad846dd0e4bbea6f7f7f

Then use:
Authorization: Token @token


═════════════════════════════════════════════════════════════════
TOKEN AUTHENTICATION COMPARISON
═════════════════════════════════════════════════════════════════

❌ BEFORE (INCORRECT):
Authorization: Bearer YOUR_TOKEN_HERE

✅ AFTER (CORRECT):
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6f7f7f


═════════════════════════════════════════════════════════════════
API CATEGORIES & REQUIREMENTS
═════════════════════════════════════════════════════════════════

1️⃣  Authentication (6 APIs)
   ├─ POST   /auth/login/              [PUBLIC - NO TOKEN]
   ├─ GET    /auth/profile/            [REQUIRES TOKEN]
   ├─ PUT    /auth/profile/            [REQUIRES TOKEN]
   ├─ POST   /auth/change-password/    [REQUIRES TOKEN]
   ├─ POST   /auth/logout/             [REQUIRES TOKEN]
   └─ POST   /auth/refresh-token/      [REQUIRES TOKEN]

2️⃣  Students (6 APIs) [ALL REQUIRE TOKEN]
   ├─ GET    /students/
   ├─ GET    /students/{id}/
   ├─ GET    /students/{id}/attendance/
   ├─ GET    /students/{id}/marks/
   ├─ GET    /students/{id}/fees/
   └─ GET    /students/{id}/fee-payments/

3️⃣  Faculty (5 APIs) [ALL REQUIRE TOKEN]
   ├─ GET    /departments/
   ├─ GET    /courses/
   ├─ GET    /subjects/
   ├─ GET    /classes/
   └─ GET    /teachers/{id}/subjects/

4️⃣  Attendance (3 APIs) [ALL REQUIRE TOKEN]
   ├─ GET    /attendance/
   ├─ POST   /attendance/
   └─ DELETE /attendance/{id}/

5️⃣  Fees (4 APIs) [ALL REQUIRE TOKEN]
   ├─ POST   /fees/payments/
   ├─ GET    /fees/payments/?student_id={id}
   ├─ GET    /fees/payments/student_due/?student_id={id}
   └─ POST   /fees/payments/send_reminder/

6️⃣  Marks/Exams (8 APIs) [ALL REQUIRE TOKEN]
   ├─ GET    /marks/
   ├─ POST   /marks/
   ├─ GET    /marks/{id}/
   ├─ PUT    /marks/{id}/
   ├─ DELETE /marks/{id}/
   ├─ GET    /marks/by_student/?student_id={id}
   ├─ GET    /marks/by_subject/?subject_id={id}
   └─ GET    /results/?student_id={id}

7️⃣  Notifications (4 APIs) [ALL REQUIRE TOKEN]
   ├─ GET    /notifications/
   ├─ GET    /notifications/{id}/
   ├─ PUT    /notifications/{id}/mark_read/
   └─ DELETE /notifications/{id}/


═════════════════════════════════════════════════════════════════
TROUBLESHOOTING
═════════════════════════════════════════════════════════════════

Problem: "Authentication credentials were not provided"
Solution: Add the Authorization header with valid token

Problem: "Invalid token" or "Token does not exist"
Solution: Make sure you copied the token correctly from login response

Problem: Getting 401 Unauthorized on every request
Solution: 
1. Check if token is copied correctly
2. Token might be expired (login again)
3. Verify Authorization header format: "Token <value>"

Problem: Login returns 401 "Invalid credentials"
Solution: Check if email/password combination is correct in database


═════════════════════════════════════════════════════════════════
EXAMPLE: Full Request with Token
═════════════════════════════════════════════════════════════════

GET http://127.0.0.1:8000/api/v1/students/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6f7f7f
Content-Type: application/json


Response (200 OK):
[
  {
    "id": 1,
    "roll_number": "CS001",
    "course": 1,
    "course_name": "Bachelor of Computer Science",
    "class_enrolled": 1,
    "semester": 1,
    "dob": "2005-01-15",
    "contact_number": "9876543210",
    "address": "123 Main St",
    "category": "GENERAL",
    "user": {
      "id": 1,
      "first_name": "Rutuja",
      "last_name": "Kumar",
      "email": "rutuja@gmail.com",
      "phone": "9876543210",
      "dob": "2005-01-15",
      "role": "student"
    }
  }
]


═════════════════════════════════════════════════════════════════
✅ ALL 36 APIs READY FOR TESTING!
═════════════════════════════════════════════════════════════════
