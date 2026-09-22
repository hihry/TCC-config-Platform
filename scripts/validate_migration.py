import json
import glob
import os

def validate_schemas():
    input_files = glob.glob("repo/programs/*.json")
    for file in input_files:
        with open(file, "r") as f:
            data = json.load(f)
            assert "program" in data, f"Missing 'program' in {file}"
            assert "rules" in data, f"Missing 'rules' in {file}"
            for rule in data["rules"]:
                assert "perspective" in rule
                assert "direction" in rule
                assert "stepper" in rule
    print(f"Validation successful: All {len(input_files)} program JSON files passed schema validation.")

if __name__ == "__main__":
    validate_schemas()
