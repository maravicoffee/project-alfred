#!/usr/bin/env python3.11
"""
Project Alfred - Comprehensive Feature Testing
Tests all endpoints and features
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
TEST_USER = "test-user-complete"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_tools():
    """Test tools listing"""
    print("\n=== Testing Tools Endpoint ===")
    response = requests.get(f"{BASE_URL}/tools")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Tools available: {len(data['tools'])}")
    for tool in data['tools']:
        print(f"  - {tool['name']}: {tool['description']}")
    return response.status_code == 200

def test_chat():
    """Test chat endpoint"""
    print("\n=== Testing Chat Endpoint ===")
    messages = [
        "Hello Alfred!",
        "What's 25 + 17?",
        "Can you search for information about AI agents?"
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": msg, "user_id": TEST_USER}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"Alfred: {data['response']}")
            if 'metadata' in data and 'suggestions' in data.get('metadata', {}):
                suggestions = data['metadata']['suggestions']
                if suggestions:
                    print(f"Suggestions: {len(suggestions)} available")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        time.sleep(1)
    
    return True

def test_conversations():
    """Test conversation management"""
    print("\n=== Testing Conversation Management ===")
    
    # List conversations
    response = requests.get(f"{BASE_URL}/api/conversations/{TEST_USER}")
    print(f"Conversations: {response.status_code}")
    if response.status_code == 200:
        convos = response.json()
        print(f"  Found {len(convos.get('conversations', []))} conversations")
    
    return response.status_code == 200

def test_personalization():
    """Test personalization features"""
    print("\n=== Testing Personalization ===")
    
    # Get profile
    print("\n1. Getting user profile...")
    response = requests.get(f"{BASE_URL}/api/personalization/profile/{TEST_USER}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        profile = response.json()
        print(json.dumps(profile, indent=2))
    
    # Get preferences
    print("\n2. Getting preferences...")
    response = requests.get(f"{BASE_URL}/api/personalization/profile/{TEST_USER}/preferences")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        prefs = response.json()
        print(json.dumps(prefs, indent=2))
    
    # Update preference
    print("\n3. Updating preference...")
    response = requests.post(
        f"{BASE_URL}/api/personalization/profile/{TEST_USER}/preferences",
        json={"key": "communication_style", "value": "professional"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(response.json())
    
    # Get suggestions
    print("\n4. Getting suggestions...")
    response = requests.get(f"{BASE_URL}/api/personalization/suggestions/{TEST_USER}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        suggestions = response.json()
        print(json.dumps(suggestions, indent=2))
    
    # Get insights
    print("\n5. Getting insights...")
    response = requests.get(f"{BASE_URL}/api/personalization/insights/{TEST_USER}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        insights = response.json()
        print(json.dumps(insights, indent=2))
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("PROJECT ALFRED - COMPREHENSIVE FEATURE TEST")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Tools Listing", test_tools),
        ("Chat & Cognitive Loop", test_chat),
        ("Conversation Management", test_conversations),
        ("Personalization & Digital Twin", test_personalization)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    main()
