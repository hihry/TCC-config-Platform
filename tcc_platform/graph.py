import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from langgraph.graph import StateGraph, END
from tcc_platform.state import AgentState
from tcc_platform.agents.planner import run_planner
from tcc_platform.agents.editor import run_editor
from tcc_platform.agents.qa import run_qa
from tcc_platform.agents.gitops import run_gitops

def route_after_qa(state: AgentState):
    if state.get("is_valid"):
        return "gitops"
    else:
        if state.get("iterations", 0) > 3:
            return END
        return "editor"
        
def route_after_planner(state: AgentState):
    if not state.get("target_rule"):
        return END
    return "editor"

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", run_planner)
    workflow.add_node("editor", run_editor)
    workflow.add_node("qa", run_qa)
    workflow.add_node("gitops", run_gitops)
    
    workflow.set_entry_point("planner")
    
    workflow.add_conditional_edges(
        "planner",
        route_after_planner,
        {"editor": "editor", END: END}
    )
    
    workflow.add_edge("editor", "qa")
    
    workflow.add_conditional_edges(
        "qa",
        route_after_qa,
        {"gitops": "gitops", "editor": "editor", END: END}
    )
    
    workflow.add_edge("gitops", END)
    
    return workflow.compile()
