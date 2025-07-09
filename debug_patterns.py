#!/usr/bin/env python3
import json

USER_DATA_FILE = "user_data.json"
with open(USER_DATA_FILE, 'r') as f:
    user_data = json.load(f)

def test_personalize_prompt(user_input):
    name = user_data.get("name", "Friend")
    lower_input = user_input.lower()
    
    print(f"Input: '{user_input}'")
    print(f"Lower: '{lower_input}'")
    print(f"Contains 'show family': {'show family' in lower_input}")
    print(f"Contains 'show contact': {'show contact' in lower_input}")
    
    # Direct show commands (check these first to avoid conflicts)
    if "show family" in lower_input:
        family = user_data.get("family", [])
        if family:
            return f"Your family: {', '.join(family)}"
        else:
            return "No family members saved."
    
    if "show contact" in lower_input:
        contacts = user_data.get("contacts", {})
        if contacts:
            contact_list = []
            for name, info in contacts.items():
                contact_list.append(f"{name}: {info}")
            return f"Your contacts: {'; '.join(contact_list)}"
        else:
            return "No contacts saved."
    
    return "Not matched"

# Test cases
print("=== Testing show family ===")
result = test_personalize_prompt("show family")
print(f"Result: {result}")

print("\n=== Testing show contacts ===")
result = test_personalize_prompt("show contacts")
print(f"Result: {result}")

print(f"\nFamily data: {user_data.get('family', [])}")
print(f"Contacts data: {user_data.get('contacts', {})}")
