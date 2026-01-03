## 👨‍🏫 TEACHER API DOCUMENTATION

### Overview
This guide explains all the APIs available for teachers in the ERP system. Teachers can view their assigned courses, manage student attendance, view and manage student marks, and access student information.

---

## 🔐 Authentication

**All endpoints require authentication** (except login).

**Header Format:**
```
Authorization: Token <auth_token>
```

**Get Token:**
```http
POST http://127.0.0.1:8000/api/v1/auth/login/
Content-Type: application/json

{
  "email": "teacher@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "auth_token": "7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p",
  "user_id": 5,
  "email": "teacher@example.com",
  "first_name": "Dr.",
  "last_name": "Smith",
  "role": "faculty",
  "message": "Login successful"
}
```

---

## 👥 FACULTY & COURSE ENDPOINTS (5 APIs)

### 1. LIST ALL DEPARTMENTS
**Request Type:** GET  
**Endpoint:** `/departments/`  
**Authentication:** Required ✅  
**Purpose:** View all departments in the institution

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/departments/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Computer Science"
  },
  {
    "id": 2,
    "name": "Electronics"
  },
  {
    "id": 3,
    "name": "Mechanical Engineering"
  },
  {
    "id": 4,
    "name": "Civil Engineering"
  }
]
```

---

### 2. LIST ALL COURSES
**Request Type:** GET  
**Endpoint:** `/courses/`  
**Authentication:** Required ✅  
**Purpose:** View all available courses/programs

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/courses/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Bachelor of Computer Science",
    "department": 1,
    "department_name": "Computer Science"
  },
  {
    "id": 2,
    "name": "Bachelor of Electronics",
    "department": 2,
    "department_name": "Electronics"
  },
  {
    "id": 3,
    "name": "Bachelor of Mechanical Engineering",
    "department": 3,
    "department_name": "Mechanical Engineering"
  }
]
```

---

### 3. LIST ALL SUBJECTS
**Request Type:** GET  
**Endpoint:** `/subjects/`  
**Authentication:** Required ✅  
**Purpose:** View all subjects/courses across all departments

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/subjects/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Data Structures",
    "code": "DS101",
    "semester": 1,
    "department": 1,
    "department_name": "Computer Science",
    "course": 1,
    "course_name": "Bachelor of Computer Science",
    "teacher": 5,
    "teacher_name": "Dr. Smith"
  },
  {
    "id": 2,
    "name": "Web Development",
    "code": "WD201",
    "semester": 2,
    "department": 1,
    "department_name": "Computer Science",
    "course": 1,
    "course_name": "Bachelor of Computer Science",
    "teacher": 6,
    "teacher_name": "Prof. Johnson"
  },
  {
    "id": 3,
    "name": "Database Management",
    "code": "DB301",
    "semester": 3,
    "department": 1,
    "department_name": "Computer Science",
    "course": 1,
    "course_name": "Bachelor of Computer Science",
    "teacher": 5,
    "teacher_name": "Dr. Smith"
  }
]
```

---

### 4. LIST ALL CLASSES
**Request Type:** GET  
**Endpoint:** `/classes/`  
**Authentication:** Required ✅  
**Purpose:** View all class divisions (semester, section groupings)

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/classes/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "department": 1,
    "department_name": "Computer Science",
    "section": "A",
    "semester": 1
  },
  {
    "id": 2,
    "department": 1,
    "department_name": "Computer Science",
    "section": "B",
    "semester": 1
  },
  {
    "id": 3,
    "department": 1,
    "department_name": "Computer Science",
    "section": "A",
    "semester": 2
  }
]
```

---

### 5. GET YOUR ASSIGNED SUBJECTS
**Request Type:** GET  
**Endpoint:** `/teachers/{id}/subjects/`  
**Authentication:** Required ✅  
**Purpose:** View all subjects assigned to you

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/teachers/5/subjects/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Data Structures",
    "code": "DS101",
    "semester": 1,
    "department": 1,
    "department_name": "Computer Science",
    "course": 1,
    "course_name": "Bachelor of Computer Science",
    "teacher": 5,
    "teacher_name": "Dr. Smith"
  },
  {
    "id": 3,
    "name": "Database Management",
    "code": "DB301",
    "semester": 3,
    "department": 1,
    "department_name": "Computer Science",
    "course": 1,
    "course_name": "Bachelor of Computer Science",
    "teacher": 5,
    "teacher_name": "Dr. Smith"
  }
]
```

---

## 📋 ATTENDANCE ENDPOINTS (3 APIs)

### 1. LIST ATTENDANCE RECORDS
**Request Type:** GET  
**Endpoint:** `/attendance/`  
**Authentication:** Required ✅  
**Purpose:** View all attendance records (can filter by student_id)

**Request (All Records):**
```http
GET http://127.0.0.1:8000/api/v1/attendance/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Request (Filter by Student):**
```http
GET http://127.0.0.1:8000/api/v1/attendance/?student_id=1
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "student": 1,
    "student_roll": "CS001",
    "subject": 1,
    "subject_code": "DS101",
    "date": "2026-01-03",
    "status": true,
    "classes_held": 2,
    "classes_attended": 2,
    "marked_by": 5,
    "teacher_name": "Dr. Smith"
  },
  {
    "id": 2,
    "student": 1,
    "student_roll": "CS001",
    "subject": 1,
    "subject_code": "DS101",
    "date": "2026-01-02",
    "status": false,
    "classes_held": 1,
    "classes_attended": 0,
    "marked_by": 5,
    "teacher_name": "Dr. Smith"
  },
  {
    "id": 3,
    "student": 2,
    "student_roll": "CS002",
    "subject": 1,
    "subject_code": "DS101",
    "date": "2026-01-03",
    "status": true,
    "classes_held": 2,
    "classes_attended": 2,
    "marked_by": 5,
    "teacher_name": "Dr. Smith"
  }
]
```

---

### 2. MARK ATTENDANCE
**Request Type:** POST  
**Endpoint:** `/attendance/`  
**Authentication:** Required ✅  
**Purpose:** Record attendance for students in your class

**Request:**
```http
POST http://127.0.0.1:8000/api/v1/attendance/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json

{
  "student": 1,
  "subject": 1,
  "date": "2026-01-03",
  "status": true,
  "classes_held": 2,
  "classes_attended": 2,
  "marked_by": 5
}
```

**Response (201 Created):**
```json
{
  "id": 4,
  "student": 1,
  "student_roll": "CS001",
  "subject": 1,
  "subject_code": "DS101",
  "date": "2026-01-03",
  "status": true,
  "classes_held": 2,
  "classes_attended": 2,
  "marked_by": 5,
  "teacher_name": "Dr. Smith"
}
```

**Error Response (400 Bad Request - Duplicate Entry):**
```json
{
  "non_field_errors": ["The fields student, subject, date must make a unique set."]
}
```

**Error Response (400 Bad Request - Missing Field):**
```json
{
  "student": ["This field is required."],
  "subject": ["This field is required."]
}
```

---

### 3. DELETE ATTENDANCE RECORD
**Request Type:** DELETE  
**Endpoint:** `/attendance/{id}/`  
**Authentication:** Required ✅  
**Purpose:** Delete/correct an attendance record

**Request:**
```http
DELETE http://127.0.0.1:8000/api/v1/attendance/1/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (204 No Content):**
```
(Empty response - just status 204)
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

## 📊 MARKS/GRADES ENDPOINTS (8 APIs)

### 1. LIST ALL MARKS
**Request Type:** GET  
**Endpoint:** `/marks/`  
**Authentication:** Required ✅  
**Purpose:** View all marks in the system

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/marks/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "student": 1,
    "student_roll": "CS001",
    "subject": 1,
    "subject_code": "DS101",
    "subject_name": "Data Structures",
    "internal_marks": 40,
    "semester_marks": 60,
    "total_marks": 100
  },
  {
    "id": 2,
    "student": 2,
    "student_roll": "CS002",
    "subject": 1,
    "subject_code": "DS101",
    "subject_name": "Data Structures",
    "internal_marks": 38,
    "semester_marks": 58,
    "total_marks": 96
  }
]
```

---

### 2. CREATE MARKS ENTRY
**Request Type:** POST  
**Endpoint:** `/marks/`  
**Authentication:** Required ✅  
**Purpose:** Add marks for a student in your subject

**Request:**
```http
POST http://127.0.0.1:8000/api/v1/marks/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json

{
  "student": 1,
  "subject": 1,
  "internal_marks": 40,
  "semester_marks": 60
}
```

**Response (201 Created):**
```json
{
  "id": 5,
  "student": 1,
  "student_roll": "CS001",
  "subject": 1,
  "subject_code": "DS101",
  "subject_name": "Data Structures",
  "internal_marks": 40,
  "semester_marks": 60,
  "total_marks": 100
}
```

**Error Response (400 Bad Request):**
```json
{
  "internal_marks": ["Ensure this value is less than or equal to 50."]
}
```

---

### 3. GET MARK DETAILS
**Request Type:** GET  
**Endpoint:** `/marks/{id}/`  
**Authentication:** Required ✅  
**Purpose:** View specific mark entry details

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/marks/1/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "id": 1,
  "student": 1,
  "student_roll": "CS001",
  "subject": 1,
  "subject_code": "DS101",
  "subject_name": "Data Structures",
  "internal_marks": 40,
  "semester_marks": 60,
  "total_marks": 100
}
```

---

### 4. UPDATE MARKS
**Request Type:** PUT  
**Endpoint:** `/marks/{id}/`  
**Authentication:** Required ✅  
**Purpose:** Update/correct marks for a student

**Request:**
```http
PUT http://127.0.0.1:8000/api/v1/marks/1/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json

{
  "internal_marks": 42,
  "semester_marks": 65
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "student": 1,
  "student_roll": "CS001",
  "subject": 1,
  "subject_code": "DS101",
  "subject_name": "Data Structures",
  "internal_marks": 42,
  "semester_marks": 65,
  "total_marks": 107
}
```

---

### 5. DELETE MARKS
**Request Type:** DELETE  
**Endpoint:** `/marks/{id}/`  
**Authentication:** Required ✅  
**Purpose:** Remove a marks entry

**Request:**
```http
DELETE http://127.0.0.1:8000/api/v1/marks/1/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (204 No Content):**
```
(Empty response - just status 204)
```

---

### 6. GET MARKS BY STUDENT
**Request Type:** GET  
**Endpoint:** `/marks/by_student/?student_id={id}`  
**Authentication:** Required ✅  
**Purpose:** View all marks for a specific student

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/marks/by_student/?student_id=1
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "subject": 1,
    "subject_code": "DS101",
    "subject_name": "Data Structures",
    "internal_marks": 40,
    "semester_marks": 60,
    "total_marks": 100
  },
  {
    "id": 3,
    "subject": 3,
    "subject_code": "DB301",
    "subject_name": "Database Management",
    "internal_marks": 42,
    "semester_marks": 65,
    "total_marks": 107
  }
]
```

---

### 7. GET MARKS BY SUBJECT
**Request Type:** GET  
**Endpoint:** `/marks/by_subject/?subject_id={id}`  
**Authentication:** Required ✅  
**Purpose:** View all marks for a specific subject (class performance)

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/marks/by_subject/?subject_id=1
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "student": 1,
    "student_roll": "CS001",
    "student_name": "John Doe",
    "internal_marks": 40,
    "semester_marks": 60,
    "total_marks": 100
  },
  {
    "id": 2,
    "student": 2,
    "student_roll": "CS002",
    "student_name": "Jane Smith",
    "internal_marks": 38,
    "semester_marks": 58,
    "total_marks": 96
  }
]
```

---

### 8. GET RESULT CARDS
**Request Type:** GET  
**Endpoint:** `/results/?student_id={id}`  
**Authentication:** Required ✅  
**Purpose:** Generate/view complete result card for a student

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/results/?student_id=1
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "student_id": 1,
  "roll_number": "CS001",
  "student_name": "John Doe",
  "semester": 1,
  "subjects": [
    {
      "id": 1,
      "subject": 1,
      "subject_code": "DS101",
      "subject_name": "Data Structures",
      "internal_marks": 40,
      "semester_marks": 60,
      "total_marks": 100
    }
  ],
  "total_marks": 100,
  "percentage": 100.0
}
```

---

## 📚 STUDENT INFORMATION ENDPOINTS (2 APIs)

### 1. LIST ALL STUDENTS
**Request Type:** GET  
**Endpoint:** `/students/`  
**Authentication:** Required ✅  
**Purpose:** View all students (for class management)

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/students/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
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
    "address": "123 Main Street",
    "category": "GENERAL",
    "user": {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "9876543210",
      "dob": "2005-01-15",
      "role": "student"
    }
  }
]
```

---

### 2. GET STUDENT DETAILS
**Request Type:** GET  
**Endpoint:** `/students/{id}/`  
**Authentication:** Required ✅  
**Purpose:** View complete profile of a student

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/students/1/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "id": 1,
  "roll_number": "CS001",
  "course": 1,
  "course_name": "Bachelor of Computer Science",
  "class_enrolled": 1,
  "semester": 1,
  "dob": "2005-01-15",
  "contact_number": "9876543210",
  "address": "123 Main Street",
  "category": "GENERAL",
  "user": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "dob": "2005-01-15",
    "role": "student"
  }
}
```

---

## 👤 PROFILE ENDPOINTS (4 APIs)

### 1. GET YOUR PROFILE
**Request Type:** GET  
**Endpoint:** `/auth/profile/`  
**Authentication:** Required ✅  
**Purpose:** View your teacher profile

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/auth/profile/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "id": 5,
  "first_name": "Dr.",
  "last_name": "Smith",
  "email": "teacher@example.com",
  "phone": "9876543215",
  "dob": "1980-05-20",
  "role": "faculty"
}
```

---

### 2. UPDATE YOUR PROFILE
**Request Type:** PUT  
**Endpoint:** `/auth/profile/`  
**Authentication:** Required ✅  
**Purpose:** Update your profile information

**Request:**
```http
PUT http://127.0.0.1:8000/api/v1/auth/profile/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json

{
  "first_name": "Dr.",
  "last_name": "Smith",
  "phone": "9876543215",
  "address": "Faculty Quarters, Campus",
  "dob": "1980-05-20"
}
```

**Response (200 OK):**
```json
{
  "first_name": "Dr.",
  "last_name": "Smith",
  "phone": "9876543215",
  "address": "Faculty Quarters, Campus",
  "dob": "1980-05-20"
}
```

---

### 3. CHANGE PASSWORD
**Request Type:** POST  
**Endpoint:** `/auth/change-password/`  
**Authentication:** Required ✅  
**Purpose:** Change your login password

**Request:**
```http
POST http://127.0.0.1:8000/api/v1/auth/change-password/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json

{
  "old_password": "password123",
  "new_password": "newpassword456",
  "confirm_password": "newpassword456"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

---

### 4. LOGOUT
**Request Type:** POST  
**Endpoint:** `/auth/logout/`  
**Authentication:** Required ✅  
**Purpose:** Logout and invalidate token

**Request:**
```http
POST http://127.0.0.1:8000/api/v1/auth/logout/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

---

## 🔔 NOTIFICATION ENDPOINTS (4 APIs)

### 1. LIST YOUR NOTIFICATIONS
**Request Type:** GET  
**Endpoint:** `/notifications/`  
**Authentication:** Required ✅  
**Purpose:** View all notifications sent to you

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/notifications/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "sender": 3,
    "sender_name": "Admin",
    "recipient": 5,
    "recipient_roll": "T001",
    "title": "Grades Submitted",
    "message": "Please submit remaining grades for DS101",
    "is_read": false,
    "created_at": "2026-01-03T09:00:00Z"
  }
]
```

---

### 2. GET NOTIFICATION DETAILS
**Request Type:** GET  
**Endpoint:** `/notifications/{id}/`  
**Authentication:** Required ✅  
**Purpose:** View specific notification

**Request:**
```http
GET http://127.0.0.1:8000/api/v1/notifications/1/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "id": 1,
  "sender": 3,
  "sender_name": "Admin",
  "recipient": 5,
  "recipient_roll": "T001",
  "title": "Grades Submitted",
  "message": "Please submit remaining grades for DS101",
  "is_read": false,
  "created_at": "2026-01-03T09:00:00Z"
}
```

---

### 3. MARK NOTIFICATION AS READ
**Request Type:** PUT  
**Endpoint:** `/notifications/{id}/mark_read/`  
**Authentication:** Required ✅  
**Purpose:** Mark notification as read

**Request:**
```http
PUT http://127.0.0.1:8000/api/v1/notifications/1/mark_read/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "id": 1,
  "sender": 3,
  "sender_name": "Admin",
  "recipient": 5,
  "recipient_roll": "T001",
  "title": "Grades Submitted",
  "message": "Please submit remaining grades for DS101",
  "is_read": true,
  "created_at": "2026-01-03T09:00:00Z"
}
```

---

### 4. DELETE NOTIFICATION
**Request Type:** DELETE  
**Endpoint:** `/notifications/{id}/`  
**Authentication:** Required ✅  
**Purpose:** Delete a notification

**Request:**
```http
DELETE http://127.0.0.1:8000/api/v1/notifications/1/
Authorization: Token 7c3f4b9d8e2a1c6f5h4j2k1l9m8n7o6p
Content-Type: application/json
```

**Response (204 No Content):**
```
(Empty response - just status 204)
```

---

## 📊 HTTP STATUS CODES

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK - Request successful | Data retrieved/updated |
| 201 | Created - Resource created | Mark entry created |
| 204 | No Content - Success, no body | Record deleted |
| 400 | Bad Request - Invalid data | Missing/invalid fields |
| 401 | Unauthorized - Invalid token | Token missing/expired |
| 403 | Forbidden - Not allowed | Accessing restricted data |
| 404 | Not Found - Resource missing | Student ID doesn't exist |
| 500 | Server Error | Database error |

---

## 💡 BEST PRACTICES FOR TEACHERS

1. **Always use token** in Authorization header
2. **Verify student IDs** before recording data
3. **Double-check marks** before submitting
4. **Update attendance regularly** for accurate tracking
5. **Keep password secure** and change periodically
6. **Use meaningful data** - invalid entries affect students

---

## 📝 TYPICAL TEACHER WORKFLOW

1. **Login** → Get auth_token
2. **View Your Subjects** → Get assigned courses
3. **List Students** → See all enrolled students
4. **Mark Attendance** → Record daily attendance
5. **Enter Marks** → Input student grades
6. **Review Results** → Generate result cards
7. **Check Notifications** → Read important messages
8. **Logout** → End session

---

## 🔐 SECURITY NOTES

✅ **DO:**
- Keep token confidential
- Verify student information
- Update grades accurately
- Logout when done
- Change password regularly

❌ **DON'T:**
- Share your login credentials
- Expose your token
- Enter fake attendance/marks
- Leave session active unattended

---

**Total Accessible APIs for Teachers: 23**
- 5 Faculty/Course APIs
- 3 Attendance APIs
- 8 Marks APIs
- 2 Student Info APIs
- 4 Profile/Auth APIs
- 4 Notification APIs
