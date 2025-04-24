# Rate Limiting Implementation and Testing

## Overview

This document describes the implementation and testing of rate limiting features to protect the application against potential DoS (Denial of Service) attacks.

## Implementation Details

### 1. Rate Limiting Configuration
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Limiter using the remote address as the key
limiter = Limiter(key_func=get_remote_address)

# Bind the limiter to the Flask app
limiter.init_app(app)
```

### 2. Protected Routes
```python
@app.route('/ManagerLogin', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Rate limit: 5 requests per minute per IP
def managerLogin():
    # ... login logic
```

## Testing Methodology

### Test Setup
- Two Flask applications are run:
  - **Rate-limited version** (`main.py`) on port 5001
  - **Non-rate-limited version** (`main_no_ratelimit.py`) on port 5002
- The test script [`attack_scripts/rate_limit_test.py`] is used to simulate concurrent login attempts to both endpoints.
- The script sends 50 total requests to each endpoint, with up to 5 concurrent requests at a time, and prints results for each request.

### Test Parameters
```python
# Test configuration in attack_scripts/rate_limit_test.py
NUM_REQUESTS = 50      # Total requests to send
CONCURRENT_REQUESTS = 5  # Number of concurrent requests
RATE_LIMITED_URL = "http://127.0.0.1:5001/ManagerLogin"
NON_RATE_LIMITED_URL = "http://127.0.0.1:5002/ManagerLogin"
```

### Output Example
The script prints a table comparing the result of each request side by side:

| Request # | Rate Limited Version | Non-Rate Limited Version |
|-----------|---------------------|-------------------------|
| 1         | Success             | Success                 |
| 2         | Success             | Success                 |
| ...       | ...                 | ...                     |

A summary table is also printed at the end, showing the count of successful, rate-limited, and error responses for each endpoint.

## Test Results

### Rate-Limited Version (Port 5001)
- First 5 requests successful
- Subsequent requests rate-limited (HTTP 429)
- Results:
  - Total Requests: 30
  - Successful: 5
  - Rate Limited: 25
  - Other Errors: 0

### Non-Rate-Limited Version (Port 5002)
- All requests successful
- No rate limiting protection
- Results:
  - Total Requests: 30
  - Successful: 30
  - Rate Limited: 0
  - Other Errors: 0

## Security Benefits

1. **DoS Protection**
   - Limits rapid-fire login attempts
   - Prevents server overload from automated attacks
   - Maintains service availability for legitimate users

2. **Brute Force Prevention**
   - Restricts number of login attempts
   - Makes password guessing attacks impractical
   - Adds time delay between attempts

3. **Resource Conservation**
   - Prevents database overload
   - Reduces server CPU usage
   - Maintains application responsiveness

## Implementation Considerations

1. **Rate Limit Parameters**
   - 5 requests per minute chosen as balance between security and usability
   - Can be adjusted based on specific requirements
   - Different limits possible for different endpoints

2. **Storage Backend**
   - Currently using in-memory storage (development)
   - Production should use Redis or similar for distributed setup
   - Warning logged about production recommendations

3. **Client Identification**
   - Using IP address for rate limiting
   - Could be extended to use other identifiers
   - Consider proxy/VPN implications

## Future Improvements

1. **Enhanced Rate Limiting**
   - Add rate limiting to other sensitive endpoints
   - Implement different limits for different user roles
   - Add burst allowance for legitimate high-traffic periods

2. **Monitoring**
   - Add metrics collection for rate-limited requests
   - Implement alerting for repeated limit violations
   - Track patterns of rate limit hits

3. **Client Feedback**
   - Add Retry-After headers
   - Improve rate limit exceeded messages
   - Implement progressive delays

## Testing Validation
The implementation successfully demonstrates:
- Effective request rate control
- Proper limit enforcement
- Clear distinction between protected and unprotected endpoints
- Reliable rate limit counting
- Appropriate HTTP status codes
