import urllib.request
import urllib.error
import json
import sys

def check_app():
    print("Checking running application...")
    base_url = "http://127.0.0.1:8000"
    
    # 1. Check Health
    try:
        print(f"GET {base_url}/health")
        with urllib.request.urlopen(f"{base_url}/health") as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print(f"✅ Application is healthy! Records: {data.get('records')}")
            else:
                print(f"❌ Application returned status {response.status}")
                sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ Failed to connect: {e}")
        print("Make sure the application is running on port 8000.")
        sys.exit(1)

    # 2. Test Search
    test_question = "who created python?"
    print(f"\nPOST {base_url}/ask - Question: '{test_question}'")
    
    try:
        req = urllib.request.Request(
            f"{base_url}/ask",
            data=json.dumps({"question": test_question}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✅ Answer: {result.get('answer')}")
    except Exception as e:
        print(f"❌ Error asking question: {e}")
        sys.exit(1)

    print("\n✅ Verification Successful!")

if __name__ == "__main__":
    check_app()
