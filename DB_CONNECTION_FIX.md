# Database Connection Issue Resolution

## Issue Description

The Flask application was encountering HTTP 500 errors when attempting to connect to the MySQL database. The specific error messages revealed two main issues:

1. **Table Name Case Sensitivity**
   - Error: `Table 'onlinesystem.manager' doesn't exist`
   - The SQLAlchemy model was looking for table `manager` (lowercase)
   - The actual MySQL table was named `Manager` (uppercase M)

2. **Password Hashing**
   - Error: `ValueError: Invalid salt`
   - The stored password in the database was not properly bcrypt-hashed
   - This caused the password verification to fail with an invalid salt error

## Resolution Steps

### 1. Table Name Case Fix
```python
class Manager(db.Model):
    __tablename__ = 'Manager'  # Explicitly set the table name
    __table_args__ = {'extend_existing': True}  # Allow table to be redefined
    # ... rest of the model definition
```

The fix involved:
- Explicitly setting `__tablename__` to match the exact case in MySQL
- Adding `__table_args__` to handle table redefinition gracefully

### 2. Password Hashing Fix
```sql
UPDATE Manager SET pword='$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY.fs1r0OPLbPie' WHERE username='ABC';
```

The fix involved:
- Updating the stored password with a properly bcrypt-hashed version
- Ensuring the password hash format matches Flask-Bcrypt's expectations

## Additional Improvements

1. **Debug Logging**
   - Added detailed logging in the login route to track authentication steps
   - Makes it easier to diagnose similar issues in the future

2. **Error Handling**
   - Improved the login route to handle user not found cases separately
   - Better password verification logic with explicit conditions

## Lessons Learned

1. **Case Sensitivity**
   - MySQL table names are case-sensitive in some environments
   - Always explicitly specify table names in SQLAlchemy models
   - Use consistent casing across database schema and application code

2. **Password Storage**
   - Always use proper password hashing before storing in database
   - Verify hash format matches the hashing library's expectations
   - Use bcrypt with proper salt generation for password hashing

3. **Debugging**
   - Implement detailed logging for authentication processes
   - Check both application logs and database logs for issues
   - Test with valid credentials after making database changes

## Testing Confirmation

After implementing these fixes:
- Login requests with valid credentials succeed
- Rate limiting functions as expected (5 requests per minute)
- No more HTTP 500 errors from database connection issues
- Password verification works correctly with hashed passwords
