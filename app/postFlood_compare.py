import requests
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import sys

def send_request(url, request_num, batch_num):
    try:
        response = requests.post(url, data={
            'username': 'admin',
            'pword': 'admin123'
        })
        
        if response.status_code == 429:  # Rate limit exceeded
            result = "Rate Limited!"
        elif response.status_code == 500:  # Server error
            result = "Error 500"
        elif response.status_code == 200:  # Success
            result = "Success"
        else:
            result = f"Error {response.status_code}"
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Batch {batch_num} - {url.split(':')[2]}: Request {request_num}: {result}")
        return result
        
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Batch {batch_num} - {url.split(':')[2]}: Request {request_num}: Connection Error")
        return "Error"

def run_batch(batch_num, urls, requests_per_batch):
    results = {url: {"success": 0, "rate_limited": 0, "errors": 0} for url in urls}
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        print(f"\nStarting batch {batch_num}...")
        
        for request_num in range(1, requests_per_batch + 1):
            for url in urls:
                result = executor.submit(send_request, url, request_num, batch_num).result()
                
                if result == "Success":
                    results[url]["success"] += 1
                elif result == "Rate Limited!":
                    results[url]["rate_limited"] += 1
                else:
                    results[url]["errors"] += 1
        
        print(f"Batch {batch_num} completed")
        if batch_num < total_batches:
            print(f"Waiting {batch_delay} seconds before next batch...")
            time.sleep(batch_delay)
    
    return results

# Test configuration
urls = [
    "http://127.0.0.1:5001/ManagerLogin",  # Rate limited version
    "http://127.0.0.1:5002/ManagerLogin"   # Non-rate limited version
]
requests_per_batch = 10
total_batches = 3
batch_delay = 2  # seconds between batches

print("Starting DoS comparison test")
print("Testing both rate-limited (5001) and non-rate-limited (5002) versions")
print(f"Will send {requests_per_batch} requests per batch, {total_batches} batches")
print("-" * 50)

total_results = {url: {"success": 0, "rate_limited": 0, "errors": 0} for url in urls}

for batch in range(1, total_batches + 1):
    batch_results = run_batch(batch, urls, requests_per_batch)
    for url in urls:
        for metric in ["success", "rate_limited", "errors"]:
            total_results[url][metric] += batch_results[url][metric]

print("\n" + "=" * 50)
print("Attack Summary:")
print("=" * 50)

for url in urls:
    port = url.split(":")[2]
    version = "Rate Limited" if "5001" in url else "No Rate Limit"
    print(f"\nVersion: {version} (Port {port})")
    print(f"Total Requests: {sum(total_results[url].values())}")
    print(f"Successful: {total_results[url]['success']}")
    print(f"Rate Limited: {total_results[url]['rate_limited']}")
    print(f"Other Errors: {total_results[url]['errors']}")
    print("-" * 30)
