#!/usr/bin/env python3
"""
Test script to demonstrate the validation system preventing dummy/test data
"""

import requests
import json

# Test data - mix of valid and invalid entries
test_cases = [
    # Should be BLOCKED
    {"prompt": "add task a", "expected": "blocked", "reason": "too short"},
    {"prompt": "add task test", "expected": "blocked", "reason": "dummy pattern"},
    {"prompt": "add goal dummy", "expected": "blocked", "reason": "dummy pattern"},
    {"prompt": "add expense 45 for kill", "expected": "blocked", "reason": "dummy pattern"},
    {"prompt": "remind me to test something", "expected": "blocked", "reason": "test pattern"},
    {"prompt": "add task buy groceries", "expected": "blocked", "reason": "duplicate"},
    
    # Should be ALLOWED
    {"prompt": "add task study for exam", "expected": "allowed", "reason": "valid content"},
    {"prompt": "add goal learn guitar", "expected": "allowed", "reason": "valid content"},
    {"prompt": "add expense 12 for bus fare", "expected": "allowed", "reason": "valid content"},
    {"prompt": "remind me to call dentist", "expected": "allowed", "reason": "valid content"},
]

def test_validation():
    print("🛡️  Testing Personal Assistant Validation System")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{test['prompt']}'")
        print(f"   Expected: {test['expected']} ({test['reason']})")
        
        try:
            response = requests.post(
                "http://localhost:8001/chat",
                headers={"Content-Type": "application/json"},
                json={"prompt": test['prompt']}
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                # Check if response indicates success or failure
                is_blocked = any(word in response_text.lower() for word in 
                               ['failed', 'invalid', 'already exists', 'too short', 'dummy', 'test'])
                
                if test['expected'] == 'blocked' and is_blocked:
                    print(f"   ✅ PASS: Correctly blocked")
                    passed += 1
                elif test['expected'] == 'allowed' and not is_blocked:
                    print(f"   ✅ PASS: Correctly allowed")
                    passed += 1
                else:
                    print(f"   ❌ FAIL: Expected {test['expected']}, got opposite")
                    print(f"      Response: {response_text}")
                    failed += 1
            else:
                print(f"   ❌ ERROR: HTTP {response.status_code}")
                failed += 1
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"🏆 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Validation system is working perfectly.")
    else:
        print("⚠️  Some tests failed. Check the validation rules.")

if __name__ == "__main__":
    test_validation()
