import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from tools.json_editor import patch_rule
import uuid

def run_gitops(state):
    print("--- GITOPS NODE ---")
    
    target_rule = state.get("target_rule")
    patch_data = state.get("patch_data")
    
    if not target_rule or not patch_data:
        return {"status": "GitOps skipped."}
        
    program = target_rule["program"]
    rule_index = target_rule["rule_index"]
    
    # Apply patch locally (mocking git checkout/commit)
    try:
        patch_rule(program, rule_index, patch_data)
        
        # Mock PR creation
        pr_id = str(uuid.uuid4())[:8]
        pr_url = f"https://github.com/mock-org/tcc-config/pull/{pr_id}"
        print(f"Committed change locally and raised mock PR: {pr_url}")
        
        return {
            "pr_url": pr_url,
            "status": "GitOps PR Created."
        }
    except Exception as e:
        return {"status": f"GitOps Error: {str(e)}"}
