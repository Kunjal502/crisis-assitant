def response_node(state):
    """
    Generate response based on state.
    Returns a dict with message and emergency flag.
    """
    # Check if emergency is triggered
    if hasattr(state, 'emergency_triggered') and state.emergency_triggered:
        return {
            "message": "🚨 You may need immediate financial support. Please consider reaching verified financial support resources.",
            "emergency": True
        }
    
    # Check if state has emergency flag set
    if state.emergency:
        return {
            "message": "Your situation seems urgent. I'm analyzing this with priority.",
            "emergency": False
        }
    
    # Try to get message from last_assessment if available
    if hasattr(state, 'last_assessment') and state.last_assessment:
        try:
            message = state.last_assessment.get("next_action", {}).get("instruction_to_user", "")
            followup = state.last_assessment.get("next_action", {}).get("ask_followup", False)
            
            return {
                "message": message,
                "followup": followup,
                "emergency": False
            }
        except (AttributeError, TypeError):
            pass
    
    # Default response based on output
    if state.output:
        # Extract meaningful response from output
        if isinstance(state.output, dict):
            message_parts = []
            
            if "response" in state.output:
                return {
                    "message": state.output["response"],
                    "emergency": False
                }
            
            # Build response from available fields
            if "final_advice" in state.output:
                message_parts.append(state.output["final_advice"])
            
            if message_parts:
                return {
                    "message": " ".join(message_parts),
                    "emergency": False
                }
    
    # Fallback response
    return {
        "message": "I've analyzed your situation. Please check the details for guidance.",
        "emergency": False
    }

