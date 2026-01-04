# Token Authentication - Fixes Applied ✅

## Summary of Changes Made

### 1. **LoginSerializer Fix** ✅
**File:** [api/serializers.py](api/serializers.py#L154)

**Change:** Added validation method to convert email to username
```python
def validate(self, data):
    """Convert email to username since CustomUser uses email as username field"""
    data['username'] = data['email']
    return data
```

**Why:** Django's `authenticate()` expects `username`, but the form accepts `email`. The CustomUser model uses email as the login field.

---

### 2. **Token Response Format Fix** ✅
**File:** [api/views.py](api/views.py#L101)

**Change:** Updated login response to use `auth_token` instead of `token`
```python
# Before
return Response({'token': token.key, 'role': user.role})

# After
return Response({'auth_token': token.key, 'role': user.role})
```

**Why:** Matches the test.http file expectations and API documentation.

---

### 3. **Profile Endpoint Added** ✅
**File:** [api/views.py](api/views.py#L112)

**New Endpoint:** GET `/auth/profile/`
```python
@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
def profile(self, request):
    """Get authenticated user's profile"""
    user = request.user
    return Response({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
        'phone': user.phone,
        'address': user.address,
        'dob': user.dob,
    })
```

---

### 4. **Additional Auth Endpoints Added** ✅
**File:** [api/views.py](api/views.py)

#### a. Update Profile Endpoint
- **Endpoint:** PUT `/auth/update-profile/`
- **Auth:** Required ✅
- **Returns:** Updated user data

#### b. Change Password Endpoint (ENHANCED)
- **Endpoint:** POST `/auth/change-password/`
- **Auth:** Required ✅
- **Validates:** Old password and password match
- **Deletes:** All existing tokens to force re-login ✅

---

### 5. **Permission Classes Added to All Viewsets** ✅
**File:** [api/views.py](api/views.py)

Added `permission_classes = [IsAuthenticated]` to:
- ✅ DepartmentViewSet
- ✅ CourseViewSet
- ✅ SubjectViewSet
- ✅ ClassViewSet
- ✅ TeacherViewSet
- ✅ FeePaymentViewSet
- ✅ MarksViewSet

---

### 6. **CORS Configuration Added** ✅
**File:** [erp/settings.py](erp/settings.py#L180)

**Added:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "https://erp-9pbn.onrender.com",
    "https://*.render.com",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
```

**Why:** Fixes CORS errors when frontend on different domain accesses API.

---

## 🧪 TESTING INSTRUCTIONS

### Local Testing (Before Deployment)

#### 1. Test Login
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"email":"rishab@gmail.com","password":"rishu1234"}'
```

**Expected Response:**
```json
{
  "auth_token": "5a743e38ec213f224e20026ea1fa69a75700aa50",
  "role": "student"
}
```

#### 2. Test Profile (Using Token)
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/auth/profile/" \
  -H "Authorization: Token 5a743e38ec213f224e20026ea1fa69a75700aa50"
```

**Expected Response:**
```json
{
  "id": 1,
  "email": "rishab@gmail.com",
  "first_name": "Rishab",
  "last_name": "Kumar",
  "role": "student",
  "phone": "9876543210",
  "address": "123 Main St",
  "dob": "2000-01-01"
}
```

#### 3. Test Invalid Token
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/auth/profile/" \
  -H "Authorization: Token invalid_token"
```

**Expected Response:** 401 Unauthorized
```json
{
  "detail": "Invalid token."
}
```

#### 4. Test Missing Token
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/auth/profile/"
```

**Expected Response:** 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 🚀 Deployment Steps

### For Render.com Deployment

1. **Update settings_prod.py** (if you have it)
   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://yourdomain.com",
       "https://erp-9pbn.onrender.com",
   ]
   ```

2. **Ensure environment variables are set:**
   - `SECRET_KEY` - Keep in environment, don't hardcode
   - `DEBUG = False` - Already set ✅
   - `ALLOWED_HOSTS = ['*']` - Already set ✅

3. **Run migrations (if any):**
   ```bash
   python manage.py migrate
   ```

4. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Deploy to Render:**
   ```bash
   git add .
   git commit -m "Fix: Token authentication and CORS configuration"
   git push origin main
   ```

---

## 📋 VERIFICATION CHECKLIST

After deployment, verify:

- [ ] Login endpoint returns `auth_token` (not `token`)
- [ ] Profile endpoint returns authenticated user data
- [ ] Invalid token returns 401 error
- [ ] Missing token returns 401 error
- [ ] CORS headers present in responses
- [ ] Authorization header format: `Token <token>`
- [ ] All viewsets require authentication
- [ ] Students can only see their own data (if row-level security implemented)

---

## ❌ Common Issues & Solutions

### Issue: "Token not found" or "Invalid token"
**Solution:** 
1. Check token is being returned from login endpoint
2. Verify token format: `Authorization: Token <token>` (not `Bearer`)
3. Ensure token hasn't been deleted by logout

### Issue: CORS error in browser console
**Solution:**
1. Check `CORS_ALLOWED_ORIGINS` includes your frontend domain
2. Verify `CORS_ALLOW_CREDENTIALS = True`
3. Check response includes proper CORS headers

### Issue: "Authentication credentials were not provided"
**Solution:**
1. Include `Authorization: Token <token>` header
2. Verify token is valid and hasn't expired
3. Check request path matches authenticated endpoints

### Issue: Login fails with "Invalid credentials"
**Solution:**
1. Verify email is correct (not username)
2. Verify password is correct
3. Check user exists in database with that email

---

## 📚 API Endpoint Summary (After Fixes)

### Authentication Endpoints
| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/auth/login/` | ❌ | Get auth token |
| GET | `/auth/profile/` | ✅ | Get user profile |
| PUT | `/auth/update-profile/` | ✅ | Update profile |
| POST | `/auth/change-password/` | ✅ | Change password |
| POST | `/auth/logout/` | ✅ | Logout (delete token) |

### All Other Endpoints
- All now require authentication (`Authorization: Token <token>`) ✅

---

## 🔐 Security Improvements

1. ✅ All endpoints except login require authentication
2. ✅ Tokens are unique per user
3. ✅ Changing password deletes all tokens (forces re-login)
4. ✅ CORS properly configured for production
5. ✅ Email used as unique identifier (not username)

---

**Last Updated:** 2026-01-04  
**Status:** Ready for Production Deployment

