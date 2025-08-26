import json
import sys
from jsonschema import validate, ValidationError

SCHEMA_PATH = "skill_tree.schema.json"
DATA_PATH = "skill_tree.json"

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    try:
        schema = load(SCHEMA_PATH)
    except Exception as e:
        print(f"Failed to load schema: {e}")
        sys.exit(2)
    try:
        data = load(DATA_PATH)
    except Exception as e:
        print(f"Failed to load data: {e}")
        sys.exit(2)
    try:
        validate(instance=data, schema=schema)
        print("Validation passed: skill_tree.json conforms to skill_tree.schema.json")
    except ValidationError as ve:
        print("Validation FAILED:")
        print(ve)
        sys.exit(3)

if __name__ == '__main__':
    main()
