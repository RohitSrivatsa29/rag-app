import json
import os

filepath = "f:/rad-application/data/python_concepts.json"

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Check if already a list
    if content.startswith('[') and content.endswith(']'):
        print("File is already a JSON list.")
        valid = True
        try:
            json.loads(content)
        except:
            valid = False
            print("But it is invalid JSON.")
            
    if not content.startswith('['):
        print("Wrapping content in list...")
        # Add brackets
        new_content = f"[{content}]"
        
        # specific fix for trailing comma if present
        if content.endswith(','):
             new_content = f"[{content[:-1]}]"
             
        # validate
        try:
            json.loads(new_content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Fixed and saved.")
        except json.JSONDecodeError as e:
            print(f"Failed to fix: {e}")
            # comprehensive fix attempts
            # maybe it's missing commas between objects?
            # or has trailing commas inside?
            pass

except Exception as e:
    print(f"Error: {e}")
