import requests
from concurrent.futures import ThreadPoolExecutor

# Test settings
NUM_REQUESTS = 500  # Total requests to send
CONCURRENT_REQUESTS = 50 # Number of concurrent requests

# Target URLs
RATE_LIMITED_URL = "http://127.0.0.1:5001/ManagerLogin"
NON_RATE_LIMITED_URL = "http://127.0.0.1:5002/ManagerLogin"

def send_request(url: str, request_num: int):
    """Send a login request and return the result."""
    try:
        response = requests.post(url, data={
            'username': 'admin',
            'pword': 'admin123'
        })
        
        # Check if request was rate limited or successful
        if response.status_code == 429:
            print(f"Request {request_num}: Rate Limited")
            return "Rate Limited"
        elif response.status_code == 200:
            print(f"Request {request_num}: Success")
            return "Success"
        else:
            print(f"Request {request_num}: Error {response.status_code}")
            return "Error"
    except Exception as e:
        print(f"Request {request_num}: Connection Error: {str(e)}")
        return "Error"

def test_endpoint(url: str, name: str):
    """Test a single endpoint and collect results."""
    results = {"success": 0, "rate_limited": 0, "error": 0}
    
    print(f"\nTesting {name}...")
    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = [executor.submit(send_request, url, i) for i in range(1, NUM_REQUESTS + 1)]
        
        for future in futures:
            result = future.result()
            if result == "Success":
                results["success"] += 1
            elif result == "Rate Limited":
                results["rate_limited"] += 1
            else:
                results["error"] += 1
    
    return results

def main():
    # Test rate-limited endpoint
    rate_limited_results = test_endpoint(RATE_LIMITED_URL, "Rate Limited Version")
    
    # Test non-rate-limited endpoint
    non_rate_limited_results = test_endpoint(NON_RATE_LIMITED_URL, "Non-Rate Limited Version")
    
    # Print comparison
    print("\n=== Results Comparison ===")
    print("\nRate Limited Version (Port 5001):")
    print(f"Successful: {rate_limited_results['success']}")
    print(f"Rate Limited: {rate_limited_results['rate_limited']}")
    print(f"Errors: {rate_limited_results['error']}")
    
    print("\nNon-Rate Limited Version (Port 5002):")
    print(f"Successful: {non_rate_limited_results['success']}")
    print(f"Rate Limited: {non_rate_limited_results['rate_limited']}")
    print(f"Errors: {non_rate_limited_results['error']}")

if __name__ == "__main__":
    main()
