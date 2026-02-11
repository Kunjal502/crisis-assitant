from langgraph.graph import StateGraph
from schemas.agent_state_schema import AgentState
from nodes.reasoning_node import reasoning_node
from nodes.guard_node import guard_node
from nodes.response_node import response_node

graph = StateGraph(AgentState)

graph.add_node("reason", reasoning_node)
graph.add_node("guard", guard_node)
graph.add_node("respond", response_node)

graph.set_entry_point("reason")
graph.add_edge("reason", "guard")
graph.add_edge("guard", "respond")

agent_app = graph.compile()
