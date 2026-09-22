import json
from pydantic import BaseModel, Field
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from tools.db_retrieval import query_rules

class PlannerOutput(BaseModel):
    thought: str = Field(description="Reasoning about the request")
    sql_query: str = Field(description="DuckDB SQL query to find the target rule.")

def run_planner(state):
    print("--- PLANNER NODE ---")
    request = state["request"]
    
    # MOCK LLM LOGIC: Map request text to the correct SQL query
    req_lower = request.lower()
    if "standard" in req_lower and "exception" in req_lower:
        sql_query = "SELECT * FROM rules WHERE program='STANDARD' AND carrier_status='EXCEPTION'"
    elif "gsp" in req_lower and "leg2" in req_lower:
        sql_query = "SELECT * FROM rules WHERE program='GSP' AND leg='LEG2'"
    elif "ag" in req_lower and "delivered" in req_lower:
        sql_query = "SELECT * FROM rules WHERE program='AG' AND carrier_status='DELIVERED'"
    else:
        sql_query = "SELECT * FROM rules LIMIT 1"
        
    thought = "MOCK: Identified target conditions from request."
    print(f"Generated SQL: {sql_query}")
    
    # Execute Query (Testing real DuckDB integration)
    try:
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
            "planner_thought": thought,
            "status": status,
            "iterations": state.get("iterations", 0) + 1
        }
    except Exception as e:
        return {"status": f"Planner Error: {str(e)}"}
