# Quick Testing Guide - Token Authentication

## 🚀 Test the Fixes Locally

### Step 1: Start the Development Server
```bash
python manage.py runserver
```

---

## 📝 Test Using test.http (REST Client)

### Method A: Using VS Code REST Client Extension

1. **Open test.http file**
2. **Run Login Request** (Line 20)
   ```http
   POST http://127.0.0.1:8000/api/v1/auth/login/
   Content-Type: application/json
   
   {
     "email": "rishab@gmail.com",
     "password": "rishu1234"
   }
   ```

3. **Copy `auth_token` from response**
   - Should look like: `"auth_token": "5a743e38ec213f224e20026ea1fa69a75700aa50"`

4. **Update `@token` variable in test.http**
   ```
   @token = your_copied_token_here
   ```

5. **Run Profile Request** (Line 41)
   ```http
   GET http://127.0.0.1:8000/api/v1/auth/profile/
   Authorization: Token @token
   ```

6. **Expected Response:**
   ```json
   {
     "id": 1,
     "email": "rishab@gmail.com",
     "first_name": "Rishab",
     "last_name": "Kumar",
     "role": "student",
     "phone": "9876543210",
     "address": "Your address here",
     "dob": "2000-01-01"
   }
   ```

---

## 🐚 Test Using cURL (Command Line)

### 1. Login and Get Token
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"rishab@gmail.com","password":"rishu1234"}'
```

**Response:**
```json
{
  "auth_token": "5a743e38ec213f224e20026ea1fa69a75700aa50",
  "role": "student"
}
```

### 2. Save Token in Variable
```bash
TOKEN="5a743e38ec213f224e20026ea1fa69a75700aa50"
```

### 3. Test Profile Endpoint
```bash
curl -X GET http://127.0.0.1:8000/api/v1/auth/profile/ \
  -H "Authorization: Token $TOKEN"
```

### 4. Test with Invalid Token (Should Fail)
```bash
curl -X GET http://127.0.0.1:8000/api/v1/auth/profile/ \
  -H "Authorization: Token invalid_token_123"
```

**Expected Error:**
```json
{
  "detail": "Invalid token."
}
```

### 5. Test without Token (Should Fail)
```bash
curl -X GET http://127.0.0.1:8000/api/v1/auth/profile/
```

**Expected Error:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 6. Test Update Profile
```bash
curl -X PUT http://127.0.0.1:8000/api/v1/auth/update-profile/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated Name",
    "phone": "9999999999"
  }'
```

### 7. Test Change Password
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/change-password/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "rishu1234",
    "new_password": "newpass1234",
    "confirm_password": "newpass1234"
  }'
```

### 8. Test Logout (Delete Token)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/logout/ \
  -H "Authorization: Token $TOKEN"
```

**Response:**
```json
{
  "detail": "Successfully logged out."
}
```

### 9. Try Using Deleted Token (Should Fail)
```bash
curl -X GET http://127.0.0.1:8000/api/v1/auth/profile/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Error:**
```json
{
  "detail": "Invalid token."
}
```

---

## ✅ Complete Test Checklist

Run through these tests to verify everything works:

- [ ] **Login** - Returns `auth_token`
- [ ] **Profile** - Returns authenticated user data
- [ ] **Update Profile** - Updates user info successfully
- [ ] **Change Password** - Changes password and deletes token
- [ ] **Logout** - Deletes token successfully
- [ ] **Invalid Token** - Returns 401 error
- [ ] **Missing Token** - Returns 401 error
- [ ] **Student List** - Returns 401 (requires auth)
- [ ] **Marks List** - Returns 401 (requires auth)
- [ ] **Attendance List** - Returns 401 (requires auth)

---

## 🔍 Debugging Tips

### Check if Token Exists in Database
```bash
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token
from accounts.models import CustomUser

# List all tokens
for token in Token.objects.all():
    print(f"User: {token.user.email}, Token: {token.key}")

# Check specific user
user = CustomUser.objects.get(email="rishab@gmail.com")
token = Token.objects.get(user=user)
print(token.key)
```

### Check User Authentication
```python
from django.contrib.auth import authenticate

user = authenticate(username="rishab@gmail.com", password="rishu1234")
if user:
    print("✅ Authentication works!")
else:
    print("❌ Authentication failed!")
```

### Test Token Authentication
```python
from rest_framework.authtoken.models import Token

# Get token
token = Token.objects.get(key="5a743e38ec213f224e20026ea1fa69a75700aa50")
print(f"Token user: {token.user.email}")
print(f"Token is valid: {token.created}")
```

---

## 📊 Test Results Summary

After running all tests, you should see:

```
✅ Login endpoint returns auth_token
✅ Profile endpoint requires authentication
✅ Invalid tokens are rejected
✅ All viewsets require authentication
✅ CORS headers are present (if testing from different domain)
✅ Token-based auth is working correctly
```

---

## 🚀 Ready for Render Deployment

Once all tests pass:

1. Commit changes
   ```bash
   git add .
   git commit -m "Fix: Token authentication flow and CORS"
   ```

2. Push to main branch
   ```bash
   git push origin main
   ```

3. Render will auto-deploy

4. Test on production:
   ```bash
   curl https://erp-9pbn.onrender.com/api/v1/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"email":"rishab@gmail.com","password":"rishu1234"}'
   ```

---

**Version:** 1.0  
**Last Updated:** 2026-01-04

