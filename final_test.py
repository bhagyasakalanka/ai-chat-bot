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

print("🧪 FINAL COMPREHENSIVE TEST - Simplified Personal Assistant\n")

print("📋 TASK MANAGEMENT:")
test_endpoint("add task: prepare annual budget", "Adding task")
test_endpoint("what are my tasks", "Listing all tasks")
test_endpoint("complete task: test new task", "Completing task")

print("\n⏰ REMINDER & SCHEDULE:")
test_endpoint("add reminder: dentist appointment", "Adding reminder")
test_endpoint("schedule 2025-07-12: client presentation", "Adding schedule")
test_endpoint("my reminders", "Listing reminders")

print("\n👥 CONTACT & FAMILY:")
test_endpoint("add contact Lisa: lisa@work.com", "Adding contact")
test_endpoint("what are my contacts", "Listing contacts")
test_endpoint("find emma", "Finding specific contact")
test_endpoint("my family", "Listing family")

print("\n🎯 GOALS & NOTES:")
test_endpoint("add goal: read 12 books this year", "Adding goal")
test_endpoint("add note: great restaurant downtown", "Adding note")
test_endpoint("my goals", "Listing goals")

print("\n💰 EXPENSES:")
test_endpoint("add expense 15: coffee", "Adding expense")
test_endpoint("show expenses", "Expense summary")

print("\n🤖 AI QUERIES:")
test_endpoint("how's my productivity today?", "AI general query")
test_endpoint("what should I prioritize?", "AI advice query")

print("\n✅ COMPREHENSIVE TEST COMPLETE!")
