import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
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
        
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    structured_llm = llm.with_structured_output(EditorOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI configuration editor. Your job is to decide which fields to patch based on the user request. \nTarget Rule: {target_rule}\nPrevious QA Errors (if any): {errors}"),
        ("user", "Request: {request}")
    ])
    
    chain = prompt | structured_llm
    
    try:
        response = chain.invoke({
            "target_rule": target_rule,
            "request": request,
            "errors": validation_errors
        })
        
        patch_data = {}
        
        # Apply semantic search to find exact keys
        if response.new_message_intent:
            matches = semantic_search(response.new_message_intent, "MESSAGE", top_k=1)
            if matches:
                patch_data["message_key"] = matches[0]["key"]
                
        if response.new_alert_intent:
            matches = semantic_search(response.new_alert_intent, "ALERT", top_k=1)
            if matches:
                patch_data["alert_key"] = matches[0]["key"]
                
        print(f"Proposed Patch Data: {patch_data}")
        return {
            "patch_data": patch_data,
            "editor_thought": response.thought,
            "status": "Editor proposed patch."
        }
    except Exception as e:
        return {"status": f"Editor Error: {str(e)}"}
