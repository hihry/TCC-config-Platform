from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    # Input
    request: str
    
    # Planner
    sql_query: Optional[str]
    target_rule: Optional[Dict[str, Any]]
    planner_thought: Optional[str]
    
    # Editor
    patch_data: Optional[Dict[str, Any]]
    editor_thought: Optional[str]
    
    # QA
    is_valid: bool
    validation_errors: List[str]
    
    # GitOps
    pr_url: Optional[str]
    
    # Control
    status: str
    iterations: int
