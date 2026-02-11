from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class AgentState(BaseModel):
    user_input: str
    steps: int = 5
    emergency: bool = False
    output: Optional[Dict[str, Any]] = None
    current_step: int = 0
    completed_steps: List[Dict[str, Any]] = []
    needs_reevaluation: bool = False
    emergency_triggered: bool = False
    history: List[Dict[str, Any]] = []
    last_assessment: Optional[Dict[str, Any]] = None
