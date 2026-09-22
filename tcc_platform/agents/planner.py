import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from tools.db_retrieval import query_rules

class PlannerOutput(BaseModel):
    thought: str = Field(description="Reasoning about the request")
    sql_query: str = Field(description="DuckDB SQL query to find the target rule. Table is 'rules'. Columns: program, rule_index, perspective, direction, leg, carrier_status, message_key, alert_key")

def run_planner(state):
    print("--- PLANNER NODE ---")
    request = state["request"]
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    structured_llm = llm.with_structured_output(PlannerOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI planner for a shipment tracking config system. Your job is to convert the user's natural language request into a DuckDB SQL query to find the exact rule they want to edit.\nTable: rules\nColumns: program, rule_index, perspective, direction, leg, carrier_status, message_key, alert_key, stepper."),
        ("user", "Request: {request}")
    ])
    
    chain = prompt | structured_llm
    
    try:
        response = chain.invoke({"request": request})
        sql_query = response.sql_query
        print(f"Generated SQL: {sql_query}")
        
        # Execute Query
        results = query_rules(sql_query)
        if isinstance(results, dict) and "error" in results:
            target_rule = None
            status = f"Planner SQL Error: {results['error']}"
        elif len(results) == 0:
            target_rule = None
            status = "Planner found no matching rules."
        else:
            target_rule = results[0] # Take first match
            status = "Planner found target rule."
            
        return {
            "sql_query": sql_query,
            "target_rule": target_rule,
            "planner_thought": response.thought,
            "status": status,
            "iterations": state.get("iterations", 0) + 1
        }
    except Exception as e:
        return {"status": f"Planner Error: {str(e)}"}
