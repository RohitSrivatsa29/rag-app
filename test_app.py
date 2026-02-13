"""
Test script to verify RAG application functionality
Run this after setup to ensure everything is working correctly
"""

import requests
import json
import sys
import time

def test_health_endpoint():
    """Test the /health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Records: {data['records']}")
            print(f"   Index Ready: {data['index_ready']}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print("   Make sure the application is running: python app.py")
        return False

def test_ask_endpoint():
    """Test the /ask endpoint"""
    print("\nTesting /ask endpoint...")
    
    test_questions = [
        "What is this?",
        "Tell me about Python",
        "How does this work?"
    ]
    
    for question in test_questions:
        print(f"\n  Question: {question}")
        try:
            response = requests.post(
                "http://localhost:8000/ask",
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data['answer']
                print(f"  ✅ Got answer ({len(answer)} chars)")
                print(f"     Preview: {answer[:100]}...")
            else:
                print(f"  ❌ Request failed with status {response.status_code}")
                print(f"     Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ Request failed: {e}")
            return False
    
    return True

def test_frontend():
    """Test if frontend is accessible"""
    print("\nTesting frontend...")
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200 and "RAG Assistant" in response.text:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend check failed")
            return False
    except Exception as e:
        print(f"❌ Frontend check failed: {e}")
        return False

def check_data_files():
    """Check if data files exist"""
    print("\nChecking data files...")
    import os
    
    if not os.path.exists("data"):
        print("❌ data/ folder not found")
        return False
    
    json_files = [f for f in os.listdir("data") if f.endswith('.json')]
    
    if not json_files:
        print("⚠️  No JSON files found in data/ folder")
        print("   Application will work but have no knowledge to search")
        return True
    
    print(f"✅ Found {len(json_files)} JSON file(s):")
    for f in json_files:
        size = os.path.getsize(f"data/{f}")
        print(f"   - {f} ({size} bytes)")
    
    return True

def check_database():
    """Check if database exists and has records"""
    print("\nChecking database...")
    import os
    import sqlite3
    
    if not os.path.exists("knowledge.db"):
        print("⚠️  Database not found (will be created on first run)")
        return True
    
    try:
        conn = sqlite3.connect("knowledge.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM knowledge")
        count = cursor.fetchone()[0]
        conn.close()
        
        print(f"✅ Database has {count} records")
        return True
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def check_frontend_build():
    """Check if frontend is built"""
    print("\nChecking frontend build...")
    import os
    
    if not os.path.exists("frontend/dist"):
        print("❌ Frontend not built")
        print("   Run: cd frontend && npm run build")
        return False
    
    if not os.path.exists("frontend/dist/index.html"):
        print("❌ Frontend build incomplete")
        print("   Run: cd frontend && npm run build")
        return False
    
    print("✅ Frontend is built")
    return True

def main():
    print("=" * 60)
    print("RAG Application Test Suite")
    print("=" * 60)
    print()
    
    # Pre-flight checks (don't require server running)
    print("PRE-FLIGHT CHECKS")
    print("-" * 60)
    
    preflight_passed = True
    preflight_passed &= check_data_files()
    preflight_passed &= check_database()
    preflight_passed &= check_frontend_build()
    
    print()
    print("SERVER TESTS (requires app to be running)")
    print("-" * 60)
    print("Make sure to run 'python app.py' in another terminal")
    print()
    
    input("Press Enter when server is running...")
    
    # Give server time to start
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    # Server tests
    server_passed = True
    server_passed &= test_health_endpoint()
    server_passed &= test_frontend()
    server_passed &= test_ask_endpoint()
    
    print()
    print("=" * 60)
    if preflight_passed and server_passed:
        print("✅ ALL TESTS PASSED!")
        print()
        print("Your application is ready to deploy!")
        print("See DEPLOYMENT.md for deployment instructions")
    elif preflight_passed and not server_passed:
        print("⚠️  Pre-flight checks passed but server tests failed")
        print("Make sure the server is running: python app.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please fix the issues above before deploying")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
