import csv
import json
import os
from collections import defaultdict

def migrate():
    input_file = "repo/MAIN.csv"
    output_dir = "repo/programs/"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    programs = defaultdict(list)
    
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            program = row["program"]
            
            # Extract dense stepper array
            steps = []
            for i in range(11):
                step_key = f"STEP_{i}"
                if row.get(step_key):
                    steps.append(row[step_key])
            
            rule = {
                "perspective": row["perspective"],
                "direction": row["direction"],
                "leg": row["leg"],
                "carrier_status": row["carrier_status"],
                "message_key": row["message_key"],
                "alert_key": row["alert_key"],
                "stepper": steps
            }
            programs[program].append(rule)
            
    for program, rules in programs.items():
        output_path = os.path.join(output_dir, f"{program}.json")
        with open(output_path, "w") as f:
            json.dump({"program": program, "rules": rules}, f, indent=2)
            
    print(f"Migrated MAIN.csv into {len(programs)} program JSON files.")

if __name__ == "__main__":
    migrate()
