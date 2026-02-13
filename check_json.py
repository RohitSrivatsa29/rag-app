import json
import sys
import os

def check_file(filepath):
    print(f"Checking {filepath}...")
    if not os.path.exists(filepath):
        print("  File not found!")
        return

    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Check for BOM
        if content.startswith(b'\xef\xbb\xbf'):
            print("  WARNING: File has UTF-8 BOM. This might cause issues in some tools.")
            content = content[3:]
        
        text = content.decode('utf-8')
        
        # Check for duplicate keys
        def dict_raise_on_duplicates(ordered_pairs):
            d = {}
            for k, v in ordered_pairs:
                if k in d:
                    print(f"  ERROR: Duplicate key found: {k}")
                d[k] = v
            return d

        data = json.loads(text, object_pairs_hook=dict_raise_on_duplicates)
        print("  Syntax: Valid")
        print(f"  Item count: {len(data)}")
        
        if isinstance(data, list):
             print("  Structure: List (Correct)")
        else:
             print("  Structure: Object (Might be unexpected if list required)")

    except json.JSONDecodeError as e:
        print(f"  ERROR: JSON Decode Error at line {e.lineno}, column {e.colno}: {e.msg}")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    files = [
        "f:/rad-application/data/java_concepts.json",
        "f:/rad-application/data/python_concepts.json",
        "f:/rad-application/data/tech_personalities.json"
    ]
    for f in files:
        check_file(f)
