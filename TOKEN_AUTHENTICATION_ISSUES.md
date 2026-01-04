# Token Authentication Issues & Solutions

## 🔴 CRITICAL ISSUES FOUND

### Issue 1: **LoginSerializer Missing Email-to-Username Conversion**
**Location:** [api/serializers.py](api/serializers.py#L154)

**Problem:**
```python
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
```

The serializer accepts an `email` field, but Django's `authenticate()` function expects `username`.

**Current Login Flow (BROKEN):**
```python
user = authenticate(username=ser.validated_data['email'], password=...)
# ❌ Trying to authenticate with email as username - FAILS!
```

**Solution:** Add validation to the LoginSerializer to use email as username:
```python
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        # CustomUser uses email as the username field
        data['username'] = data['email']
        return data
```

---

### Issue 2: **CORS Configuration Missing**
**Location:** [erp/settings.py](erp/settings.py)

**Problem:** No CORS headers configuration for the rendered server. When frontend on different domain accesses the API, the browser blocks the request.

**Add to settings.py:**
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://*.render.com",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True
```

---

### Issue 3: **Token Authentication Missing from Public Endpoints**
**Location:** [api/views.py](api/views.py#L32)

**Problem:** Some viewsets don't have explicit permission classes:
```python
class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]  # ✅ Good
```

But these are missing:
```python
class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    # ❌ No permission_classes defined!
```

**Solution:** Add to viewsets that need authentication or make them public explicitly.

---

### Issue 4: **Missing Student Profile Endpoint**
**Location:** [api/views.py](api/views.py#L108-L120)

**Problem:** There's no endpoint for authenticated users to get their own profile. Looking at test.http line 41:
```http
GET http://127.0.0.1:8000/api/v1/auth/profile/
```

But this endpoint might not be implemented properly.

**Solution:** Add to AuthViewSet:
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
    })
```

---

### Issue 5: **Token Response Format Mismatch**
**Location:** [api/views.py](api/views.py#L103-L105)

**Problem:** Current response returns `token` but test.http expects `auth_token`:
```python
return Response({'token': token.key, 'role': user.role})
```

**test.http expects:**
```http
{
  "auth_token": "...",
  "role": "..."
}
```

**Solution:** Change response to match test.http format:
```python
return Response({'auth_token': token.key, 'role': user.role})
```

---

### Issue 6: **Missing Default Permission Classes**
**Location:** [erp/settings.py](erp/settings.py#L172-L179)

**Problem:** Default permission is `IsAuthenticated`, but some endpoints need to be public:
```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # ❌ Everything requires auth
    ]
}
```

**Solution:** Change to allow public access by default:
```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # ✅ Allow public by default
    ]
}
```

Then explicitly add `permission_classes = [IsAuthenticated]` to endpoints that need it.

---

## ✅ CORRECT AUTHENTICATION FLOW (After Fixes)

1. **Login Request:**
   ```http
   POST /api/v1/auth/login/
   Content-Type: application/json
   
   {
     "email": "user@example.com",
     "password": "password123"
   }
   ```

2. **Login Response:**
   ```json
   {
     "auth_token": "5a743e38ec213f224e20026ea1fa69a75700aa50",
     "role": "student"
   }
   ```

3. **Authenticated Request:**
   ```http
   GET /api/v1/auth/profile/
   Authorization: Token 5a743e38ec213f224e20026ea1fa69a75700aa50
   ```

4. **Response:**
   ```json
   {
     "id": 1,
     "email": "user@example.com",
     "first_name": "John",
     "last_name": "Doe",
     "role": "student",
     "phone": "9876543210",
     "address": "123 Main St"
   }
   ```

---

## 🔧 IMPLEMENTATION STEPS

1. **Fix LoginSerializer** - Add email-to-username conversion
2. **Fix Token Response Format** - Return `auth_token` instead of `token`
3. **Add Profile Endpoint** - Create auth/profile endpoint
4. **Fix Permission Classes** - Change default to `AllowAny` and set explicit permissions
5. **Add CORS Configuration** - Enable CORS for Render.com domain
6. **Test Locally** - Run test.http requests locally first
7. **Deploy** - Update settings_prod.py for production

---

## 🧪 TESTING CHECKLIST

- [ ] Login returns proper `auth_token`
- [ ] Token header format: `Authorization: Token <token>`
- [ ] Profile endpoint returns authenticated user data
- [ ] Invalid token returns 401 Unauthorized
- [ ] Missing token returns 401 Unauthorized
- [ ] CORS headers present in responses
- [ ] API works on Render.com domain

