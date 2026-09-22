import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pydantic import BaseModel, Field
from typing import Optional
from tools.localization_editor import semantic_search

class EditorOutput(BaseModel):
    thought: str = Field(description="Reasoning about what fields to change.")
    new_message_intent: Optional[str] = Field(description="The natural language intent for the new message, if requested.")
    new_alert_intent: Optional[str] = Field(description="The natural language intent for the new alert, if requested.")

def run_editor(state):
    print("--- EDITOR NODE ---")
    request = state["request"]
    target_rule = state.get("target_rule")
    validation_errors = state.get("validation_errors", [])
    
    if not target_rule:
        return {"status": "Editor skipped, no target rule."}
        
    # MOCK LLM LOGIC: Map request text to semantic intents
    req_lower = request.lower()
    new_message_intent = None
    new_alert_intent = None
    
    if "weather" in req_lower:
        new_alert_intent = "Shipping delayed due to weather."
    elif "global hub" in req_lower:
        new_message_intent = "Your item is on the way to the global shipping hub."
    elif "authentication center" in req_lower:
        new_message_intent = "Your item has been delivered to the authentication center."
    elif "action is required" in req_lower:
        new_alert_intent = "Action required: review authentication results."
    elif "delay in shipping" in req_lower:
        new_message_intent = "There is a delay in shipping your item."
        
    thought = "MOCK: Identified patch intents from request."
    
    patch_data = {}
    
    # Apply semantic search to find exact keys (Testing real sentence-transformers!)
    try:
        if new_message_intent:
            matches = semantic_search(new_message_intent, "MESSAGE", top_k=1)
            if matches:
                patch_data["message_key"] = matches[0]["key"]
                
        if new_alert_intent:
            matches = semantic_search(new_alert_intent, "ALERT", top_k=1)
            if matches:
                patch_data["alert_key"] = matches[0]["key"]
                
        print(f"Proposed Patch Data: {patch_data}")
        return {
            "patch_data": patch_data,
            "editor_thought": thought,
            "status": "Editor proposed patch."
        }
    except Exception as e:
        return {"status": f"Editor Error: {str(e)}"}
