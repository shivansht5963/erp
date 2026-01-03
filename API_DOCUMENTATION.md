# ERP System API Documentation

## Overview
This document describes all 36 REST API endpoints available in the ERP System. All endpoints are authenticated and require an API key unless otherwise specified.

**Base URL**: `/api/v1/`

---

## 1. STUDENT ENDPOINTS (6 APIs)

### List All Students
- **URL**: `GET /students/`
- **Description**: Retrieve list of all students with basic information
- **Response**: List of student objects with user details
- **Query Params**: None

### Get Student Details
- **URL**: `GET /students/{id}/`
- **Description**: Retrieve detailed information for a specific student
- **Response**: Student object with all fields
- **Params**: `id` - Student ID

### Get Student Attendance
- **URL**: `GET /students/{id}/attendance/`
- **Description**: Retrieve attendance records for a specific student
- **Response**: List of attendance records with subject names and dates
- **Params**: `id` - Student ID

### Get Student Marks
- **URL**: `GET /students/{id}/marks/`
- **Description**: Retrieve marks/grades for a specific student
- **Response**: List of marks with subject information
- **Params**: `id` - Student ID

### Get Student Fee Status
- **URL**: `GET /students/{id}/fees/`
- **Description**: Get current fee status and payment information
- **Response**: Fee status object with total due and paid amounts
- **Params**: `id` - Student ID

### Get Student Fee Payment History
- **URL**: `GET /students/{id}/fee-payments/`
- **Description**: Retrieve payment history for a student
- **Response**: List of fee payments ordered by date
- **Params**: `id` - Student ID

---

## 2. FACULTY/FACULTY ENDPOINTS (5 APIs)

### List All Departments
- **URL**: `GET /departments/`
- **Description**: Retrieve all departments
- **Response**: List of department objects

### List All Courses
- **URL**: `GET /courses/`
- **Description**: Retrieve all courses with department information
- **Response**: List of course objects

### List All Subjects
- **URL**: `GET /subjects/`
- **Description**: Retrieve all subjects with course and teacher information
- **Response**: List of subject objects

### List All Classes
- **URL**: `GET /classes/`
- **Description**: Retrieve all classes with department and semester info
- **Response**: List of class objects

### Get Teacher's Subjects
- **URL**: `GET /teachers/{id}/subjects/`
- **Description**: Get all subjects assigned to a specific teacher
- **Response**: List of subjects taught by the teacher
- **Params**: `id` - Teacher ID

---

## 3. ATTENDANCE ENDPOINTS (3 APIs)

### List All Attendance Records
- **URL**: `GET /attendance/`
- **Description**: List all attendance records
- **Query Params**: `student_id` (optional) - Filter by student
- **Response**: List of attendance records with student and subject details

### Mark Attendance
- **URL**: `POST /attendance/`
- **Description**: Create a new attendance record
- **Request Body**:
  ```json
  {
    "student": 1,
    "subject": 1,
    "date": "2025-01-03",
    "status": true,
    "classes_held": 2,
    "classes_attended": 2,
    "marked_by": 1
  }
  ```
- **Response**: Created attendance object with ID

### Delete Attendance
- **URL**: `DELETE /attendance/{id}/`
- **Description**: Remove an attendance record
- **Params**: `id` - Attendance ID
- **Response**: 204 No Content

---

## 4. FEES ENDPOINTS (4 APIs)

### Record Fee Payment
- **URL**: `POST /fees/payments/`
- **Description**: Record a new fee payment
- **Request Body**:
  ```json
  {
    "student": 1,
    "amount": "5000.00",
    "payment_date": "2025-01-03",
    "payment_method": "bank_transfer",
    "transaction_id": "TXN12345",
    "status": "paid"
  }
  ```
- **Response**: Created payment object

### Get Student Payment History
- **URL**: `GET /fees/payments/?student_id=X`
- **Description**: Retrieve all payments made by a student
- **Query Params**: `student_id` - Student ID (required)
- **Response**: List of payment records ordered by date

### Calculate Student Due Fees
- **URL**: `GET /fees/student_due/?student_id=X`
- **Description**: Get current fee dues for a student
- **Query Params**: `student_id` - Student ID (required)
- **Response**: Fee status with due and paid amounts

### Send Fee Reminder
- **URL**: `POST /fees/send_reminder/`
- **Description**: Send email reminder to student about pending fees
- **Request Body**:
  ```json
  {
    "student_id": 1
  }
  ```
- **Response**: Confirmation message with student email

---

## 5. MARKS/EXAMS ENDPOINTS (8 APIs)

### List All Marks
- **URL**: `GET /marks/`
- **Description**: Retrieve all marks records
- **Response**: List of all marks with student and subject info

### Create Marks Entry
- **URL**: `POST /marks/`
- **Description**: Create a new marks entry
- **Request Body**:
  ```json
  {
    "student": 1,
    "subject": 1,
    "internal_marks": 25,
    "semester_marks": 75
  }
  ```
- **Response**: Created marks object (total_marks calculated automatically)

### Get Specific Mark
- **URL**: `GET /marks/{id}/`
- **Description**: Retrieve a specific marks record
- **Params**: `id` - Marks ID
- **Response**: Marks object with all details

### Update Marks
- **URL**: `PUT /marks/{id}/`
- **Description**: Update an existing marks record
- **Request Body**:
  ```json
  {
    "internal_marks": 28,
    "semester_marks": 78
  }
  ```
- **Params**: `id` - Marks ID
- **Response**: Updated marks object

### Delete Marks
- **URL**: `DELETE /marks/{id}/`
- **Description**: Remove a marks record
- **Params**: `id` - Marks ID
- **Response**: 204 No Content

### Get Marks by Student
- **URL**: `GET /marks/by_student/?student_id=X`
- **Description**: Get all marks for a specific student
- **Query Params**: `student_id` - Student ID (required)
- **Response**: List of student's marks

### Get Marks by Subject
- **URL**: `GET /marks/by_subject/?subject_id=X`
- **Description**: Get all marks for a specific subject
- **Query Params**: `subject_id` - Subject ID (required)
- **Response**: List of marks for that subject

### Get Result Card
- **URL**: `GET /results/?student_id=X`
- **Description**: Generate comprehensive result card for a student
- **Query Params**: `student_id` - Student ID (required)
- **Response**:
  ```json
  {
    "student_id": 1,
    "roll_number": "CO20001",
    "student_name": "John Doe",
    "semester": 4,
    "subjects": [...],
    "total_marks": 500,
    "percentage": 85.5
  }
  ```

---

## 6. AUTHENTICATION ENDPOINTS (6 APIs)

### Login
- **URL**: `POST /auth/login/`
- **Description**: Authenticate user and get user details
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "user_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student",
    "message": "Login successful"
  }
  ```

### Logout
- **URL**: `POST /auth/logout/`
- **Description**: Logout the current user
- **Response**: Confirmation message

### Refresh Token
- **URL**: `POST /auth/refresh-token/`
- **Description**: Refresh authentication token
- **Response**: New token for continued authentication

### Get User Profile
- **URL**: `GET /auth/profile/`
- **Description**: Retrieve current logged-in user's profile
- **Response**: User object with all details

### Update User Profile
- **URL**: `PUT /auth/profile/`
- **Description**: Update current user's profile information
- **Request Body**:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "phone": "9876543210",
    "address": "123 Main St",
    "dob": "2000-01-01"
  }
  ```
- **Response**: Updated user object

### Change Password
- **URL**: `POST /auth/change-password/`
- **Description**: Change password for current user
- **Request Body**:
  ```json
  {
    "old_password": "oldpass123",
    "new_password": "newpass123",
    "confirm_password": "newpass123"
  }
  ```
- **Response**: Confirmation message

---

## 7. NOTIFICATION ENDPOINTS (4 APIs)

### List Notifications
- **URL**: `GET /notifications/`
- **Description**: Retrieve all notifications for the current user
- **Response**: List of notification objects ordered by date (newest first)

### Get Notification Details
- **URL**: `GET /notifications/{id}/`
- **Description**: Retrieve a specific notification
- **Params**: `id` - Notification ID
- **Response**: Notification object with full details

### Mark Notification as Read
- **URL**: `PUT /notifications/{id}/mark_read/`
- **Description**: Mark a notification as read
- **Params**: `id` - Notification ID
- **Response**: Updated notification object with is_read=true

### Delete Notification
- **URL**: `DELETE /notifications/{id}/`
- **Description**: Delete a notification
- **Params**: `id` - Notification ID
- **Response**: 204 No Content

---

## Error Handling

### Common Error Codes

| Code | Error | Meaning |
|------|-------|---------|
| 200 | OK | Request successful |
| 201 | Created | Resource successfully created |
| 204 | No Content | Successfully deleted |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication required or invalid |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

### Sample Error Response
```json
{
  "error": "student_id query parameter is required"
}
```

---

## Authentication

All endpoints (except login) require authentication via API Key.

**Header**: `Authorization: Api-Key YOUR_API_KEY`

---

## Response Format

All successful responses follow this format:
- **Single Object**: Returns the object
- **List**: Returns array of objects
- **Custom Endpoints**: Returns custom JSON structure as documented

---

## Rate Limiting

Currently no rate limiting is enforced. This may be implemented in future versions.

---

## Versioning

Current API Version: **v1**

Base URL: `/api/v1/`

---

## Summary

**Total APIs: 36**
- Students: 6
- Faculty: 5
- Attendance: 3
- Fees: 4
- Marks/Exams: 8
- Authentication: 6
- Notifications: 4

All endpoints are fully functional and ready for integration.
