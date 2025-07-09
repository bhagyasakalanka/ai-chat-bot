#!/usr/bin/env python3

import requests
import json

def test_endpoint(prompt, expected_contains=None):
    """Test an endpoint and optionally check if response contains expected text"""
    try:
        response = requests.post("http://localhost:8000/chat", 
                               json={"prompt": prompt},
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get("response", "")
            print(f"✅ '{prompt}' -> '{reply}'")
            
            if expected_contains and expected_contains.lower() not in reply.lower():
                print(f"⚠️  Expected '{expected_contains}' in response but got: '{reply}'")
            
            return reply
        else:
            print(f"❌ '{prompt}' -> HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ '{prompt}' -> Error: {e}")
        return None

print("🧪 Testing Personal Assistant Chatbot\n")

# Test direct data queries
print("📋 Testing Direct Data Queries:")
test_endpoint("show family", "Your family:")
test_endpoint("show contacts", "Your contacts:")
test_endpoint("show tasks", "tasks")

print("\n🤖 Testing AI Interaction:")
# Test concise AI responses (these should go to AI but be short)
test_endpoint("what time is it?")
test_endpoint("help me plan my day")

print("\n🚫 Testing Unrelated Questions:")
# Test unrelated questions (should get rejection message)
test_endpoint("what is the meaning of life?", "I'm not sure how to help")
test_endpoint("write me a poem", "I'm not sure how to help")

print("\n➕ Testing Add Operations:")
# Test adding items
test_endpoint("add task: test task")
test_endpoint("add contact John: 123-456-7890")
test_endpoint("add reminder: test reminder")

print("\n✅ Testing After Additions:")
# Verify additions worked
test_endpoint("show tasks")
test_endpoint("show contacts")
test_endpoint("show reminders")

print("\n🎉 Comprehensive test completed!")
