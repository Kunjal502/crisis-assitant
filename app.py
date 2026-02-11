from fastapi import FastAPI
from schemas.request_schema import ChatRequest
from schemas.agent_state_schema import AgentState
from nodes.reasoning_node import reasoning_node

app = FastAPI()

@app.post("/chat")
def chat(request: ChatRequest):
    state = AgentState(
        user_input=request.user_input,
        steps=request.steps,
        emergency=request.emergency
    )

    final_state = reasoning_node(state)
    return final_state.output
