import urllib.request
import json
import sys

def verify_api():
    print("Verifying API Logic...")
    base_url = "http://127.0.0.1:8000"
    
    def ask(q):
        print(f"\nQuery: '{q}'")
        req = urllib.request.Request(
            f"{base_url}/ask",
            data=json.dumps({"question": q}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                ans = result.get('answer', '')
                print(f"Answer Length: {len(ans)}")
                return ans
        except Exception as e:
            print(f"Error: {e}")
            return ""

    # 1. Ask "Who is..." -> Expect Short
    ans1 = ask("Who is Sundar Pichai")
    if len(ans1) > 0 and "Education:" not in ans1:
        print("✅ 'Who is' returned specific summary (good)")
    else:
        print(f"❌ 'Who is' returned unexpected content. Length: {len(ans1)}")
        if "Education:" in ans1: print("   (Contains Education field - too broad)")

    # 2. Ask "Tell me everything..." -> Expect Long
    ans2 = ask("Tell me everything about Sundar Pichai")
    if "Education:" in ans2 and "Career:" in ans2:
        print("✅ 'Everything' returned full profile (good)")
    else:
        print("❌ 'Everything' did not return full profile")


def test_context_retention():
    print("\nTesting Context Retention...")
    BASE_URL = "http://127.0.0.1:8000"
    
    def post_json(endpoint, payload):
        req = urllib.request.Request(
            f"{BASE_URL}{endpoint}",
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())

    # 1. Ask about Sundar Pichai
    print("Q1: Who is Sundar Pichai")
    resp1 = post_json("/ask", {"question": "Who is Sundar Pichai"})
    
    # 2. Ask about 'his education'
    print("Q2: his education")
    resp2 = post_json("/ask", {"question": "his education"})
    answer = resp2.get('answer', '')
    print(f"Answer: {answer}")
    
    assert "Sundar" in answer or "Wharton" in answer or "Stanford" in answer, "Context failed: Answer should refer to Sundar Pichai"
    assert "Andrew Ng" not in answer, "Context failed: Answer referred to Andrew Ng"
    print("✅ Context Retention Passed")

if __name__ == "__main__":
    verify_api()
    test_context_retention()
