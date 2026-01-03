## 📚 ERP API DOCUMENTATION - QUICK INDEX

**Last Updated:** January 3, 2026  
**Total APIs:** 36  
**Status:** ✅ Production Ready

---

## 🎯 FIND WHAT YOU NEED

### 👨‍💼 I'm a Student
Start here → **[STUDENT_API_DOCUMENTATION.md](STUDENT_API_DOCUMENTATION.md)**
- 14 APIs you can use
- Check grades, attendance, fees
- Update profile
- View notifications
- **Typical time to read:** 15 minutes

### 👨‍🏫 I'm a Teacher/Faculty
Start here → **[TEACHER_API_DOCUMENTATION.md](TEACHER_API_DOCUMENTATION.md)**
- 23 APIs you can use
- Mark attendance
- Enter and manage grades
- View student information
- **Typical time to read:** 20 minutes

### 👨‍💻 I'm a Developer
Start here → **[TOKEN_AUTH_SETUP.md](TOKEN_AUTH_SETUP.md)**
- Technical implementation details
- Authentication configuration
- All 36 APIs with status codes
- **Typical time to read:** 15 minutes

### ⚡ I want to test quickly
Start here → **[QUICK_START_TOKEN_GUIDE.md](QUICK_START_TOKEN_GUIDE.md)**
- Get token in 2 steps
- Test any API immediately
- Troubleshooting
- **Typical time to read:** 5 minutes

### 🧪 I want to test all APIs
Use → **[test.http](test.http)**
- All 36 APIs ready to test
- Copy-paste requests
- Just need VS Code + REST Client
- **Typical time:** 1 click per API

---

## 📊 DOCUMENTATION BREAKDOWN

| Document | Purpose | For Whom | Time | APIs |
|----------|---------|----------|------|------|
| STUDENT_API_DOCUMENTATION.md | Complete student guide | Students | 15 min | 14 |
| TEACHER_API_DOCUMENTATION.md | Complete teacher guide | Teachers | 20 min | 23 |
| TOKEN_AUTH_SETUP.md | Technical details | Developers | 15 min | 36 |
| QUICK_START_TOKEN_GUIDE.md | Quick reference | Everyone | 5 min | 36 |
| API_DOCUMENTATION_GUIDE.md | Overview & navigation | Everyone | 10 min | 36 |
| test.http | Ready-to-test APIs | Testers | - | 36 |

---

## 🔐 AUTHENTICATION (Same for Everyone)

**Step 1: Login**
```http
POST http://127.0.0.1:8000/api/v1/auth/login/
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Step 2: Copy Token**
```json
{
  "auth_token": "9944b09199c62bcf9418ad846dd0e4bbea6f7f7f"
}
```

**Step 3: Use in Requests**
```http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6f7f7f
```

---

## 🎓 API CATEGORIES

### **Students can access:**
- ✅ Student Information (6 APIs)
- ✅ Profile Management (4 APIs)
- ✅ Notifications (4 APIs)
- ❌ Attendance Management
- ❌ Grade Management
- ❌ Faculty Management

### **Teachers can access:**
- ✅ Faculty Information (5 APIs)
- ✅ Attendance Management (3 APIs)
- ✅ Grade Management (8 APIs)
- ✅ Student Information (2 APIs)
- ✅ Profile Management (4 APIs)
- ✅ Notifications (4 APIs)
- ❌ Cannot modify student data
- ❌ Cannot modify fees

### **Admins can access:**
- ✅ Everything (36 APIs)

---

## 📱 QUICK REFERENCE CARDS

### STUDENT ENDPOINTS

```
🔐 AUTHENTICATION
├─ POST   /auth/login/              [Public - No token needed]
├─ GET    /auth/profile/            [Token required]
├─ PUT    /auth/profile/            [Token required]
└─ POST   /auth/change-password/    [Token required]

📚 YOUR ACADEMICS
├─ GET    /students/{id}/marks/     [View your grades]
├─ GET    /marks/by_student/?student_id={id}
└─ GET    /results/?student_id={id} [View report card]

📋 ATTENDANCE
└─ GET    /students/{id}/attendance/ [View your attendance]

💰 FEES
├─ GET    /students/{id}/fees/      [Check fee status]
└─ GET    /students/{id}/fee-payments/ [Payment history]

🔔 NOTIFICATIONS
├─ GET    /notifications/           [View all]
├─ GET    /notifications/{id}/      [View one]
├─ PUT    /notifications/{id}/mark_read/
└─ DELETE /notifications/{id}/
```

### TEACHER ENDPOINTS

```
🔐 AUTHENTICATION (Same as students)

📚 MANAGE CLASSES
├─ GET    /departments/             [View departments]
├─ GET    /courses/                 [View courses]
├─ GET    /subjects/                [View all subjects]
├─ GET    /classes/                 [View classes]
└─ GET    /teachers/{id}/subjects/  [Your subjects]

📋 ATTENDANCE
├─ GET    /attendance/              [List all]
├─ GET    /attendance/?student_id={id} [By student]
├─ POST   /attendance/              [Mark attendance]
└─ DELETE /attendance/{id}/         [Delete record]

📊 GRADES & MARKS
├─ GET    /marks/                   [List all]
├─ POST   /marks/                   [Create entry]
├─ GET    /marks/{id}/              [View one]
├─ PUT    /marks/{id}/              [Update marks]
├─ DELETE /marks/{id}/              [Delete entry]
├─ GET    /marks/by_student/?student_id={id}
├─ GET    /marks/by_subject/?subject_id={id}
└─ GET    /results/?student_id={id} [Generate card]

👥 STUDENT INFORMATION
├─ GET    /students/                [List all students]
└─ GET    /students/{id}/           [View one student]

🔔 NOTIFICATIONS (Same as students)
```

---

## 🚀 COMMON WORKFLOWS

### **Student Workflow:**
```
1. Open test.http or use mobile app
2. Login with email & password
3. Get auth_token from response
4. Save token for future requests
5. View your marks → /students/{id}/marks/
6. Check attendance → /students/{id}/attendance/
7. Review fees → /students/{id}/fees/
8. Read notifications → /notifications/
9. Update profile if needed → PUT /auth/profile/
10. Logout when done
```

### **Teacher Workflow:**
```
1. Open test.http in VS Code
2. Login with email & password
3. Get auth_token
4. View your subjects → GET /teachers/{id}/subjects/
5. View enrolled students → GET /students/
6. Mark attendance → POST /attendance/
7. Enter marks → POST /marks/
8. Update marks if needed → PUT /marks/{id}/
9. Generate result cards → GET /results/
10. Check notifications
11. Logout
```

---

## 🆚 COMPARE DOCUMENTATION

### STUDENT_API_DOCUMENTATION.md
**Best for:** Students who need to know what they can do  
**Includes:** 14 practical APIs  
**Format:** Student-friendly, use-case driven  
**Examples:** Checking grades, viewing fees, reading notifications  
**Read time:** 15 minutes  

### TEACHER_API_DOCUMENTATION.md
**Best for:** Teachers/Faculty who need classroom management tools  
**Includes:** 23 comprehensive APIs  
**Format:** Teacher-friendly, task-oriented  
**Examples:** Marking attendance, entering grades, viewing student info  
**Read time:** 20 minutes  

### TOKEN_AUTH_SETUP.md
**Best for:** Developers and technical staff  
**Includes:** Technical implementation details  
**Format:** Technical, configuration-focused  
**Examples:** Token generation, DRF settings, authentication flow  
**Read time:** 15 minutes  

### QUICK_START_TOKEN_GUIDE.md
**Best for:** Anyone who wants to get started immediately  
**Includes:** Step-by-step quick start  
**Format:** Quick reference, easy to scan  
**Examples:** Login, token usage, basic API calls  
**Read time:** 5 minutes  

---

## 🔧 API TESTING

### Option 1: REST Client in VS Code ⭐ Recommended
- Install extension "REST Client" by Huachao Mao
- Open test.http
- Click "Send Request" above each request
- View response instantly

### Option 2: Postman
- Import test.http requests
- Set up Bearer token authentication
- Run collections
- View detailed analytics

### Option 3: cURL (Command Line)
```bash
# Login
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"password"}'

# Get students (with token)
curl -X GET http://127.0.0.1:8000/api/v1/students/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Option 4: Python Requests
```python
import requests

# Login
response = requests.post(
    'http://127.0.0.1:8000/api/v1/auth/login/',
    json={"email": "student@example.com", "password": "password"}
)
token = response.json()['auth_token']

# Get students
headers = {'Authorization': f'Token {token}'}
response = requests.get(
    'http://127.0.0.1:8000/api/v1/students/',
    headers=headers
)
print(response.json())
```

---

## ✅ VERIFICATION CHECKLIST

Before deploying, verify:
- ✅ Login works and returns token
- ✅ All student endpoints respond correctly
- ✅ All teacher endpoints respond correctly
- ✅ Token authentication working
- ✅ Status codes are correct
- ✅ Error messages are helpful
- ✅ Documentation is accurate

---

## 🆘 NEED HELP?

### Can't Login?
See: QUICK_START_TOKEN_GUIDE.md → Troubleshooting section

### Don't know which API to use?
See: STUDENT_API_DOCUMENTATION.md or TEACHER_API_DOCUMENTATION.md

### Getting 401 Unauthorized?
See: TOKEN_AUTH_SETUP.md → Token Authentication section

### Want to test APIs?
See: test.http (Just open and click "Send Request")

### Technical questions?
See: TOKEN_AUTH_SETUP.md

---

## 📞 DOCUMENTATION CONTACT

**For Documentation Updates:**
- Update the relevant .md file
- Keep examples current
- Test all examples before committing

**For API Issues:**
- Check test.http for working examples
- Review error responses in documentation
- Check status codes section

---

## 🎁 BONUS: POSTMAN COLLECTION IMPORT

To use with Postman:
1. Open Postman
2. File → Import
3. Choose test.http
4. Click Import
5. Add your token to environment variables
6. Run requests

---

## 🔄 KEEPING DOCUMENTATION UPDATED

When APIs change:
1. Update test.http first
2. Verify requests work
3. Update relevant .md file
4. Update API_DOCUMENTATION_GUIDE.md
5. Test all examples again

---

## 📊 STATISTICS

```
Total APIs:           36
├─ Students: Access  14
├─ Teachers: Access  23
└─ Admins: Access    36

Documentation Files:  5
├─ Technical:        1 (TOKEN_AUTH_SETUP.md)
├─ Quick Ref:        1 (QUICK_START_TOKEN_GUIDE.md)
├─ User Guides:      2 (STUDENT_API_DOCUMENTATION.md, TEACHER_API_DOCUMENTATION.md)
└─ Indexes:          2 (API_DOCUMENTATION_GUIDE.md, this file)

Request Examples:     100+
Response Examples:    50+
Error Examples:       20+
```

---

## 🎯 YOUR NEXT STEP

**Choose your role:**

👨‍💼 **I'm a Student** → Open [STUDENT_API_DOCUMENTATION.md](STUDENT_API_DOCUMENTATION.md)

👨‍🏫 **I'm a Teacher** → Open [TEACHER_API_DOCUMENTATION.md](TEACHER_API_DOCUMENTATION.md)

👨‍💻 **I'm a Developer** → Open [TOKEN_AUTH_SETUP.md](TOKEN_AUTH_SETUP.md)

⚡ **I want quick start** → Open [QUICK_START_TOKEN_GUIDE.md](QUICK_START_TOKEN_GUIDE.md)

🧪 **I want to test** → Open [test.http](test.http)

---

**Happy learning! 🎉**

*All 36 APIs fully documented and ready to use.*

