#!/usr/bin/env python3
import requests
import json

base_url = "http://localhost:8000/chat"

def test_api(prompt, description):
    print(f"\n🧪 Testing: {description}")
    print(f"📝 Prompt: '{prompt}'")
    
    try:
        response = requests.post(base_url, json={"prompt": prompt})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {result['response']}")
        else:
            print(f"❌ Error: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")

# Test cases
tests = [
    ("good morning", "Morning greeting"),
    ("add task: Call dentist", "Add personal task"),
    ("add work task: Review code", "Add work task"),
    ("show tasks", "View all tasks"),
    ("add reminder: Buy milk", "Add reminder"),
    ("show reminders", "View reminders"),
    ("add expense 15: Lunch", "Add expense"),
    ("show expenses", "View expenses"),
    ("add note: Important meeting notes", "Add note"),
    ("show notes", "View notes"),
    ("add goal personal: Learn Python", "Add personal goal"),
    ("show goals", "View goals"),
    ("add contact Sarah: 555-123-4567", "Add contact"),
    ("show contacts", "View contacts"),
    ("schedule 2025-07-10: Team meeting", "Add schedule item"),
    ("show today", "View today's schedule"),
    ("motivation", "Get motivation"),
    ("show family", "View family"),
    ("entertainment", "Get entertainment recommendations"),
]

print("🚀 Starting Personal Assistant API Tests")
print("=" * 50)

for prompt, description in tests:
    test_api(prompt, description)

print("\n" + "=" * 50)
print("✨ Testing completed!")
