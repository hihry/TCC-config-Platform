import json
import glob

def compile_json():
    input_files = glob.glob("repo/programs/*.json")
    compiled_rows = []
    
    for file in input_files:
        with open(file, "r") as f:
            data = json.load(f)
            program = data["program"]
            for rule in data["rules"]:
                row = {
                    "program": program,
                    "perspective": rule["perspective"],
                    "direction": rule["direction"],
                    "leg": rule["leg"],
                    "carrier_status": rule["carrier_status"],
                    "message_key": rule["message_key"],
                    "alert_key": rule.get("alert_key", "")
                }
                # Pad sparse stepper array
                for i in range(11):
                    step_key = f"STEP_{i}"
                    if i < len(rule.get("stepper", [])):
                        row[step_key] = rule["stepper"][i]
                    else:
                        row[step_key] = ""
                compiled_rows.append(row)
                
    with open("repo/compiled_main.json", "w") as f:
        json.dump(compiled_rows, f, indent=2)
        
    print(f"Compiled {len(compiled_rows)} rules into repo/compiled_main.json.")

if __name__ == "__main__":
    compile_json()
