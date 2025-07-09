#!/usr/bin/env python3

import requests
import json
import time

def test_contact_operations():
    base_url = "http://localhost:8000/chat"
    
    tests = [
        # Test natural language contact addition
        {
            "input": "add sarah phone number 0771234567 and email sarah2@test.com",
            "description": "Add contact with natural language"
        },
        # Test contact lookup variations
        {
            "input": "show sarah contact",
            "description": "Show specific contact with 'show'"
        },
        {
            "input": "find sarah contact", 
            "description": "Find specific contact with 'find'"
        },
        {
            "input": "get sarah contact",
            "description": "Get specific contact with 'get'"
        },
        # Test partial name matching
        {
            "input": "show kavindus contact",
            "description": "Show contact with partial name match"
        },
        # Test showing all contacts
        {
            "input": "show all contacts",
            "description": "Show all contacts"
        },
        # Test traditional contact addition
        {
            "input": "add contact TestUser: 0779999999",
            "description": "Add contact with traditional format"
        },
        {
            "input": "find testuser contact",
            "description": "Find traditionally added contact"
        }
    ]
    
    print("🧪 Running Contact Operations Test Suite")
    print("=" * 50)
    
    for i, test in enumerate(tests, 1):
        print(f"\n{i}. {test['description']}")
        print(f"   Input: {test['input']}")
        
        try:
            response = requests.post(base_url, json={"prompt": test['input']})
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Response: {result['response']}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print("🏁 Test suite completed!")

if __name__ == "__main__":
    test_contact_operations()
