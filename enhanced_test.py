#!/usr/bin/env python3

import requests
import json
import time

def test_enhanced_natural_language():
    base_url = "http://localhost:8000/chat"
    
    tests = [
        # Enhanced Task Operations
        {
            "input": "add task to call the doctor",
            "description": "Natural language task addition (add task to X)"
        },
        {
            "input": "create task buy milk",
            "description": "Natural language task addition (create task X)"
        },
        {
            "input": "completed call the doctor",
            "description": "Natural language task completion"
        },
        
        # Enhanced Reminder Operations
        {
            "input": "remind me to pay rent",
            "description": "Natural language reminder (remind me to X)"
        },
        {
            "input": "add reminder to water plants",
            "description": "Natural language reminder (add reminder to X)"
        },
        
        # Enhanced Goal Operations
        {
            "input": "set goal to read 20 books this year",
            "description": "Natural language goal (set goal to X)"
        },
        {
            "input": "add goal learn french",
            "description": "Natural language goal (add goal X)"
        },
        
        # Enhanced Contact Operations
        {
            "input": "add anna phone number 0771111111 and email anna@test.com",
            "description": "Natural language contact addition"
        },
        {
            "input": "show anna contact",
            "description": "Natural language contact lookup"
        },
        
        # Enhanced Note Operations
        {
            "input": "add note about project deadline",
            "description": "Natural language note (add note about X)"
        },
        {
            "input": "note that client prefers morning meetings",
            "description": "Natural language note (note that X)"
        },
        
        # Enhanced Expense Operations
        {
            "input": "spent 45 on dinner",
            "description": "Natural language expense (spent X on Y)"
        },
        {
            "input": "paid 30 for parking",
            "description": "Natural language expense (paid X for Y)"
        },
        {
            "input": "add expense 20 for coffee",
            "description": "Natural language expense (add expense X for Y)"
        },
        
        # Enhanced Schedule Operations
        {
            "input": "schedule dentist appointment on 2025-07-15",
            "description": "Natural language schedule (schedule X on DATE)"
        },
        {
            "input": "book meeting tomorrow",
            "description": "Natural language schedule (book X tomorrow)"
        },
        
        # View Operations (should still work)
        {
            "input": "show my tasks",
            "description": "View tasks"
        },
        {
            "input": "show all contacts",
            "description": "View all contacts"
        }
    ]
    
    print("🚀 Enhanced Natural Language Processing Test Suite")
    print("=" * 60)
    
    for i, test in enumerate(tests, 1):
        print(f"\n{i:2d}. {test['description']}")
        print(f"    Input: {test['input']}")
        
        try:
            response = requests.post(base_url, json={"prompt": test['input']})
            if response.status_code == 200:
                result = response.json()
                print(f"    ✅ Response: {result['response']}")
            else:
                print(f"    ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        time.sleep(0.3)  # Small delay between requests
    
    print("\n" + "=" * 60)
    print("🏁 Enhanced Natural Language Test Suite completed!")

if __name__ == "__main__":
    test_enhanced_natural_language()
