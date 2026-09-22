import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from tcc_platform.graph import build_graph

def run_evals():
    cases_path = os.path.join(os.path.dirname(__file__), '../tests/eval_cases.json')
    with open(cases_path, 'r') as f:
        eval_cases = json.load(f)
        
    graph = build_graph()
    passed = 0
    failed = 0
    
    print(f"Starting LLM Evaluation Suite with {len(eval_cases)} variations...\n")
    
    for i, test in enumerate(eval_cases):
        print(f"--- Running Eval {i+1}/{len(eval_cases)} ---")
        print(f"Prompt: '{test['prompt']}'")
        
        initial_state = {"request": test['prompt'], "iterations": 0}
        try:
            # We don't want to actually commit/PR during evals, but the mock GitOps node handles that safely.
            final_state = graph.invoke(initial_state)
            
            target = final_state.get("target_rule") or {}
            patch = final_state.get("patch_data") or {}
            
            errors = []
            
            if target.get("program") != test.get("expected_program"):
                errors.append(f"Expected program '{test.get('expected_program')}', got '{target.get('program')}'")
                
            if target.get("carrier_status") != test.get("expected_carrier_status"):
                errors.append(f"Expected status '{test.get('expected_carrier_status')}', got '{target.get('carrier_status')}'")
                
            if "expected_alert_patch" in test:
                if patch.get("alert_key") != test["expected_alert_patch"]:
                    errors.append(f"Expected alert patch '{test['expected_alert_patch']}', got '{patch.get('alert_key')}'")
                    
            if "expected_message_patch" in test:
                if patch.get("message_key") != test["expected_message_patch"]:
                    errors.append(f"Expected message patch '{test['expected_message_patch']}', got '{patch.get('message_key')}'")
                    
            if final_state.get("is_valid") is False:
                errors.append(f"Validation failed unexpectedly: {final_state.get('validation_errors')}")
                
            if not errors:
                print("PASS\n")
                passed += 1
            else:
                print("FAIL")
                for e in errors:
                    print(f"   - {e}")
                print("\n")
                failed += 1
                
        except Exception as e:
            print(f"ERROR: {e}\n")
            failed += 1
            
    print(f"--- Evaluation Results ---")
    print(f"Total: {len(eval_cases)} | Passed: {passed} | Failed: {failed}")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_evals()
