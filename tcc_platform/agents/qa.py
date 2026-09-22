import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from tools.localization_editor import validate_key

def run_qa(state):
    print("--- QA NODE ---")
    patch_data = state.get("patch_data")
    
    if not patch_data:
        return {"is_valid": True, "status": "QA Passed (No patch)"}
        
    errors = []
    
    if "message_key" in patch_data:
        key = patch_data["message_key"]
        if not validate_key(key, "MESSAGE"):
            errors.append(f"Invalid message_key: {key}")
            
    if "alert_key" in patch_data:
        key = patch_data["alert_key"]
        if not validate_key(key, "ALERT"):
            errors.append(f"Invalid alert_key: {key}")
            
    is_valid = len(errors) == 0
    
    if is_valid:
        print("QA Passed.")
        return {"is_valid": True, "validation_errors": [], "status": "QA Passed"}
    else:
        print(f"QA Failed: {errors}")
        return {"is_valid": False, "validation_errors": errors, "status": "QA Failed"}
