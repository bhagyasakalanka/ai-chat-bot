#!/usr/bin/env python3

import requests
import json

def test_endpoint(prompt, description=""):
    """Test an endpoint and show the result"""
    try:
        response = requests.post("http://localhost:8000/chat", 
                               json={"prompt": prompt},
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get("response", "")
            print(f"✅ {description}: '{prompt}' → '{reply}'")
            return reply
        else:
            print(f"❌ {description}: '{prompt}' → HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ {description}: '{prompt}' → Error: {e}")
        return None

print("🧪 Testing Enhanced Natural Language Support\n")

print("📋 TASK MANAGEMENT:")
test_endpoint("add new task: call dentist", "Adding task with 'new'")
test_endpoint("create work task: review budget", "Creating work task")
test_endpoint("what are my work tasks", "Listing work tasks")
test_endpoint("list all my tasks", "Listing all tasks")

print("\n⏰ REMINDER MANAGEMENT:")
test_endpoint("remind me to buy groceries", "Natural reminder")
test_endpoint("add new reminder: pay rent", "Adding reminder with 'new'")
test_endpoint("my reminders", "Listing reminders")

print("\n👥 CONTACT MANAGEMENT:")
test_endpoint("add new contact Alex: alex@test.com", "Adding contact with 'new'")
test_endpoint("what are my contacts", "Listing all contacts")
test_endpoint("find sarah", "Finding specific contact")

print("\n📅 SCHEDULE MANAGEMENT:")
test_endpoint("schedule 2025-07-11: team meeting", "Adding schedule item")

print("\n👪 FAMILY MANAGEMENT:")
test_endpoint("my family", "Listing family")
test_endpoint("add new family event: birthday party", "Adding family event")

print("\n✅ Enhanced Natural Language Test Complete!")
