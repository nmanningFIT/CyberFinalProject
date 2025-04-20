import requests
import time
from datetime import datetime
import sys

TARGET_URL = "http://127.0.0.1:5001/ManagerLogin"
TOTAL_REQUESTS = 30  # Total number of requests to send
REQUESTS_PER_BATCH = 10  # Number of requests to send in quick succession
BATCH_DELAY = 2  # Seconds to wait between batches

def post_flood():
    print(f"Starting DoS test against {TARGET_URL}")
    print(f"Will send {TOTAL_REQUESTS} total requests in batches of {REQUESTS_PER_BATCH}")
    print("-" * 50)

    success_count = 0
    rate_limited_count = 0
    other_error_count = 0

    for i in range(0, TOTAL_REQUESTS, REQUESTS_PER_BATCH):
        print(f"\nStarting batch {(i//REQUESTS_PER_BATCH) + 1}...")
        batch_start = datetime.now()

        # Send a batch of requests quickly
        for j in range(REQUESTS_PER_BATCH):
            if i + j >= TOTAL_REQUESTS:
                break

            try:
                response = requests.post(
                    TARGET_URL,
                    data={"username": "admin", "password": "1234"},
                    timeout=2
                )
                
                request_num = i + j + 1
                timestamp = datetime.now().strftime("%H:%M:%S")

                if response.status_code == 200:
                    print(f"[{timestamp}] Request {request_num}: Success")
                    success_count += 1
                elif response.status_code == 429:  # Rate limit exceeded
                    print(f"[{timestamp}] Request {request_num}: Rate Limited!")
                    rate_limited_count += 1
                else:
                    print(f"[{timestamp}] Request {request_num}: Error {response.status_code}")
                    other_error_count += 1

            except requests.exceptions.RequestException as e:
                print(f"Request {i + j + 1}: Failed - {str(e)}")
                other_error_count += 1

        batch_duration = (datetime.now() - batch_start).total_seconds()
        print(f"Batch completed in {batch_duration:.2f} seconds")

        # Wait between batches
        if i + REQUESTS_PER_BATCH < TOTAL_REQUESTS:
            print(f"Waiting {BATCH_DELAY} seconds before next batch...")
            time.sleep(BATCH_DELAY)

    print("\n" + "=" * 50)
    print("Attack Summary:")
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"Successful: {success_count}")
    print(f"Rate Limited: {rate_limited_count}")
    print(f"Other Errors: {other_error_count}")
    print("=" * 50)

if __name__ == "__main__":
    try:
        post_flood()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(0)