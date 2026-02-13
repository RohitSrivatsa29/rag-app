import subprocess
import time
import sys
import json
import urllib.request
import urllib.error

def verify_app():
    print("Starting application for verification...")
    # Start the application in a subprocess
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Wait for the application to start
        print("Waiting for application to become healthy...")
        max_retries = 30
        for i in range(max_retries):
            try:
                with urllib.request.urlopen("http://127.0.0.1:8000/health") as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode())
                        print(f"Application is healthy! Records: {data.get('records')}")
                        if data.get('records') == 200:
                            print("Record count verified (200).")
                        else:
                            print(f"WARNING: Record count mismatch. Expected 200, got {data.get('records')}")
                        break
            except urllib.error.URLError:
                if i == max_retries - 1:
                    print("Failed to connect to application.")
                    stdout, stderr = process.communicate(timeout=5)
                    print("STDOUT:", stdout)
                    print("STDERR:", stderr)
                    return
                time.sleep(2)
                print(f"Retrying... ({i+1}/{max_retries})")
        
        # Test Search
        print("\nTesting Search Functionality...")
        test_questions = [
            "Who created Python?",
            "What is a List Comprehension?",
            "Tell me about Alan Turing"
        ]
        
        for q in test_questions:
            print(f"\nAsking: {q}")
            req = urllib.request.Request(
                "http://127.0.0.1:8000/ask",
                data=json.dumps({"question": q}).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode())
                    print(f"Answer: {result.get('answer')}")
            except Exception as e:
                print(f"Error asking question: {e}")

    finally:
        print("\nStopping application...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("Verification complete.")

if __name__ == "__main__":
    verify_app()
