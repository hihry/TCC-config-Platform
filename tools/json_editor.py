import json
import os

def get_program_data(program_name):
    filepath = f"repo/programs/{program_name}.json"
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        return json.load(f)

def write_program_data(program_name, data):
    filepath = f"repo/programs/{program_name}.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def patch_rule(program_name, rule_index, patch_data):
    """Update specific fields in a rule."""
    data = get_program_data(program_name)
    if not data or rule_index >= len(data["rules"]):
        raise ValueError(f"Rule index {rule_index} out of bounds for program {program_name}")
    
    for key, value in patch_data.items():
        data["rules"][rule_index][key] = value
        
    write_program_data(program_name, data)
    return data["rules"][rule_index]
