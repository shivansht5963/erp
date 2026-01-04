# Token Authentication Flow Diagram

## 🔄 CORRECT AUTHENTICATION FLOW (After Fixes)

```
┌─────────────────────────────────────────────────────────────────┐
│                    BEFORE (❌ BROKEN)                           │
└─────────────────────────────────────────────────────────────────┘

CLIENT                                   SERVER
  │                                        │
  │──1. POST /auth/login/──────────────>  │
  │   {                                    │
  │     "email": "user@example.com",      │  
  │     "password": "pass123"             │
  │   }                                    │
  │                                        │
  │                               ❌ ERROR │
  │                    authenticate(      │
  │                      username=email,  │ Can't find user!
  │                      password=...     │ email ≠ username
  │                    )                  │
  │                                        │
  │<────────── 401 Unauthorized ──────────│
  │   {"error": "Invalid credentials"}    │
  │                                        │
  └───────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                    AFTER (✅ FIXED)                             │
└─────────────────────────────────────────────────────────────────┘

CLIENT                                   SERVER
  │                                        │
  │──1. POST /auth/login/──────────────>  │
  │   {                                    │
  │     "email": "user@example.com",      │  
  │     "password": "pass123"             │
  │   }                                    │
  │                                        │ ✅ LoginSerializer
  │                                        │    validate():
  │                                        │    data['username'] = data['email']
  │                                        │
  │                                        │ ✅ authenticate(
  │                                        │      username="user@example.com",
  │                                        │      password="pass123"
  │                                        │    ) → User found!
  │                                        │
  │                                        │ ✅ token, _ = 
  │                                        │    Token.objects.get_or_create()
  │                                        │
  │<────2. 200 OK ─────────────────────────│
  │   {                                    │
  │     "auth_token": "abc123def456",  ✅ │ Correct field name!
  │     "role": "student"                 │
  │   }                                    │
  │                                        │
  │────3. GET /auth/profile/ ─────────>  │
  │   Header:                              │
  │   Authorization: Token abc123def456   │
  │                                        │ ✅ TokenAuthentication
  │                                        │    Finds token in database
  │                                        │    Links to user
  │                                        │    request.user = User
  │                                        │
  │<────4. 200 OK ──────────────────────────│
  │   {                                    │
  │     "id": 1,                          │
  │     "email": "user@example.com",      │
  │     "first_name": "John",            │
  │     "role": "student",                │
  │     ...                               │
  │   }                                    │
  │                                        │
  └───────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│              COMPLETE API AUTHENTICATION FLOW                    │
└─────────────────────────────────────────────────────────────────┘

       STEP 1: LOGIN                    STEP 2: USE TOKEN
    (Get auth_token)               (Access protected resources)

┌──────────────────┐                 ┌──────────────────┐
│   CLIENT APP     │                 │   CLIENT APP     │
│                  │                 │                  │
│ Username/Email   │                 │ Saved Token:     │
│ Password input   │                 │ abc123def456     │
└────────┬─────────┘                 └────────┬─────────┘
         │                                    │
         │ POST /api/v1/auth/login/          │
         │ {                                  │
         │   "email": "user@example.com",    │
         │   "password": "pass123"            │
         │ }                                  │
         │                                    │
         ├─────────────────────────────────>┌────────────────┐
         │                                   │  DRF Router    │
         │                                   │  Auth ViewSet  │
         │                                   │  login()       │
         │                                   └────┬───────────┘
         │                                        │
         │                            ┌───────────┴──────────┐
         │                            │                      │
         │                    ┌───────▼──────┐      ┌────────▼──────┐
         │                    │ Serializer   │      │ Django Auth   │
         │                    │ validation   │      │               │
         │                    │              │      │ authenticate( │
         │                    │ email →      │      │   username,   │
         │                    │ username     │      │   password    │
         │                    │              │      │ )             │
         │                    └──────────────┘      └────────┬──────┘
         │                                                   │
         │                                        ┌──────────▼──────┐
         │                                        │  Token.objects  │
         │                                        │  .get_or_create │
         │                                        │  (user=user)    │
         │                                        └────────┬────────┘
         │                                                 │
         │<──────────────── 200 OK ──────────────────────┤
         │ {                                              │
         │   "auth_token": "abc123def456",  ✅ SAVE THIS  │
         │   "role": "student"                            │
         │ }                                              │
         │                                                 │
         │                                      STEP 2 ────┼──────────
         │                                           │     │
         │                                           │     │
         │     GET /api/v1/auth/profile/             │     │
         │     Header: Authorization: Token          │     │
         │                              abc123def456 │     │
         │                                            │     │
         ├────────────────────────────────────────────┼────>┌──────────────┐
         │                                            │     │ DRF Router   │
         │                                            │     │ Auth ViewSet │
         │                                            │     │ profile()    │
         │                                            │     └──────┬───────┘
         │                                            │            │
         │                                            │  ┌─────────▼────────┐
         │                                            │  │ TokenAuth        │
         │                                            │  │ handler:         │
         │                                            │  │                  │
         │                                            │  │ 1. Get token     │
         │                                            │  │    from header   │
         │                                            │  │ 2. Find in DB    │
         │                                            │  │ 3. Link to user  │
         │                                            │  │ request.user =   │
         │                                            │  │   User object    │
         │                                            │  └────────┬─────────┘
         │                                            │           │
         │                                            │  ┌────────▼─────┐
         │                                            │  │ Check perms:  │
         │                                            │  │ IsAuthentic.. │
         │                                            │  │ ✅ Passes     │
         │                                            │  └────────┬──────┘
         │                                            │           │
         │                                            │  ┌────────▼──────┐
         │                                            │  │ Return user    │
         │                                            │  │ profile data   │
         │                                            │  └────────┬──────┘
         │                                            │           │
         │<──────────────── 200 OK ──────────────────────────────┤
         │ {                                                      │
         │   "id": 1,                                             │
         │   "email": "user@example.com",                         │
         │   "first_name": "John",                                │
         │   "role": "student",                                   │
         │   ...                                                  │
         │ }                                                      │
         │                                                        │
         └────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│              ERROR SCENARIOS (After Fixes)                       │
└─────────────────────────────────────────────────────────────────┘

SCENARIO 1: Missing Token Header
┌──────────────────┐
│   CLIENT APP     │
│  (No Auth header)│
└────────┬─────────┘
         │
         │ GET /api/v1/auth/profile/
         │ (No Authorization header)
         │
         ├─────────────────────────>┌──────────────────┐
         │                           │ DRF Permission   │
         │                           │ Check:           │
         │                           │                  │
         │                           │ IsAuthenticated? │
         │                           │ ❌ NO            │
         │                           └────────┬─────────┘
         │                                    │
         │<────────── 401 UNAUTHORIZED ───────┤
         │ {                                  │
         │   "detail": "Authentication      │
         │    credentials were not provided"│
         │ }                                  │
         │                                    │
         └────────────────────────────────────┘

SCENARIO 2: Invalid Token
┌──────────────────┐
│   CLIENT APP     │
│  Invalid Token:  │
│  xyz999abc       │
└────────┬─────────┘
         │
         │ GET /api/v1/auth/profile/
         │ Authorization: Token xyz999abc
         │
         ├─────────────────────────>┌──────────────────┐
         │                           │ TokenAuthentic.. │
         │                           │                  │
         │                           │ Token.objects    │
         │                           │  .get(           │
         │                           │   key=xyz999abc) │
         │                           │ ❌ Not found!    │
         │                           └────────┬─────────┘
         │                                    │
         │<────────── 401 UNAUTHORIZED ───────┤
         │ {                                  │
         │   "detail": "Invalid token."      │
         │ }                                  │
         │                                    │
         └────────────────────────────────────┘

SCENARIO 3: CORS Error (Browser)
┌──────────────────────────────────────────────┐
│  FRONTEND (domain1.com)                      │
│  ┌──────────────────────────────────────┐   │
│  │ fetch('https://api.domain2.com/...')│   │
│  └──────────┬───────────────────────────┘   │
└─────────────┼──────────────────────────────┬─┘
              │                              │
              │ Origin: domain1.com          │
              │ Request CORS check           │
              │ (Browser Security)           │
              │                              │
              ├─ Different origin detected   │
              │                              │
              ├────────────────────────────> │ API (domain2.com)
              │ Preflight OPTIONS request    │ 
              │                              │
              │<───── ❌ No CORS header ─────┤
              │                              │
              │ Browser blocks response!     │
              │                              │
              │ Error in console:            │
              │ "No 'Access-Control-        │
              │  Allow-Origin' header"       │
              │                              │
         FIX: Add CORS_ALLOWED_ORIGINS in
         settings.py with frontend domain
         
         Server response should include:
         Access-Control-Allow-Origin: domain1.com
         Access-Control-Allow-Credentials: true

```

---

## 📝 Token Lifecycle

```
CREATE                 USE                    DELETE
┌────────┐          ┌─────────┐           ┌────────┐
│ Login  │ ──────> │ Requests │ ────────> │ Logout │
└────────┘          └─────────┘           └────────┘
   │                    │                     │
   │                    │                     │
   ├─ Email validated   ├─ Token in header    ├─ Token deleted
   │                    │                     │
   ├─ Password checked  ├─ Verified in DB     ├─ User must
   │                    │                     │  login again
   ├─ User found        ├─ User identified    │
   │                    │                     │
   └─ Token created     ├─ Permissions       └─ All tokens
      & saved in DB     │  checked              cleared
                        │                       (change password)
                        └─ Response sent


Token Status:
┌──────────────────────────────────┐
│ ✅ VALID                         │
│ - Created in DB                  │
│ - Matches request header         │
│ - User authenticated             │
│ - Request allowed                │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│ ❌ INVALID                       │
│ - Not in DB                      │
│ - Malformed format               │
│ - Deleted (after logout)         │
│ - Request denied (401)           │
└──────────────────────────────────┘

```

---

## 🔐 Security Measures Applied

```
┌─────────────────────────────────────────┐
│  1. EMAIL VALIDATION                    │
│  ─────────────────────────────────────  │
│  Input: "user@example.com"              │
│  Check: Valid email format ✅           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  2. CONVERT EMAIL TO USERNAME           │
│  ─────────────────────────────────────  │
│  Serializer.validate() converts:        │
│  email → username ✅                    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  3. AUTHENTICATE USER                   │
│  ─────────────────────────────────────  │
│  Django authenticate(                   │
│    username=username,                   │
│    password=password                    │
│  ) → User object or None ✅             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  4. CREATE/GET TOKEN                    │
│  ─────────────────────────────────────  │
│  Token.objects.get_or_create(           │
│    user=user                            │
│  ) → Token ✅                           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  5. STORE TOKEN IN DB                   │
│  ─────────────────────────────────────  │
│  Token(                                 │
│    key=random_string(),                 │
│    user=user,                           │
│    created=now()                        │
│  ) ✅                                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  6. SEND TOKEN TO CLIENT                │
│  ─────────────────────────────────────  │
│  Response:                              │
│  {                                      │
│    "auth_token": "abc123...",           │
│    "role": "student"                    │
│  } ✅                                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  7. VERIFY IN FUTURE REQUESTS           │
│  ─────────────────────────────────────  │
│  Header: Authorization: Token abc123   │
│                                         │
│  TokenAuthentication:                   │
│  1. Extract token from header          │
│  2. Query DB: Token.objects.get(       │
│     key=token)                         │
│  3. Match to user                      │
│  4. Check permissions                  │
│  5. Allow/Deny request ✅              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  8. INVALIDATE ON LOGOUT               │
│  ─────────────────────────────────────  │
│  Token.delete()                         │
│  Token no longer valid ✅               │
│  (Must login again)                     │
└─────────────────────────────────────────┘

```

---

This visual flow shows why your API was failing and how the fixes work!

