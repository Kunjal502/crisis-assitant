from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_input: str
    steps: Optional[int] = 5
    emergency: Optional[bool] = False
