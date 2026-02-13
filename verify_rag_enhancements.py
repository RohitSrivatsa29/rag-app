import requests
import json
import time

def test_query(question, expected_snippets=None, unpleasant_snippets=None):
    print(f"\nQuery: '{question}'")
    try:
        response = requests.post("http://localhost:8000/ask", json={"question": question})
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')
            print(f"Answer: {answer[:300]}...") # Print first 300 chars
            
            # Validation
            if expected_snippets:
                if isinstance(expected_snippets, str):
                    expected_snippets = [expected_snippets]
                
                all_found = True
                for snippet in expected_snippets:
                    if snippet.lower() not in answer.lower():
                        print(f"❌ Missing expected: '{snippet}'")
                        all_found = False
                if all_found:
                    print("✅ Positive Check Passed")
            
            if unpleasant_snippets:
                 if isinstance(unpleasant_snippets, str):
                    unpleasant_snippets = [unpleasant_snippets]
                 for snippet in unpleasant_snippets:
                     if snippet in answer: # Case sensitive check for Title
                         print(f"❌ Found unwanted: '{snippet}'")
                     else:
                         print(f"✅ Negative Check Passed (Did not find '{snippet}')")
                         
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def run_tests():
    print("Waiting for server to be ready...")
    time.sleep(2) 
    
    # Test 1: Comprehensive Answer
    print("\n--- Test 1: Comprehensive Answer ---")
    # Should contain Education AND Career/Summary
    test_query("tell me everything about Jensen Huang", ["Stanford", "NVIDIA", "Electrical Engineering"])
    
    # Test 2: Shortcuts
    print("\n--- Test 2: Shortcuts ---")
    test_query("info python lists", "ordered, mutable collections")
    
    # Test 3: No Title
    print("\n--- Test 3: No Title Format ---")
    test_query("what is python list comprehension", expected_snippets="concise way", unpleasant_snippets="**What is Python list comprehension?**")

if __name__ == "__main__":
    run_tests()
