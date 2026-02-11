from config.settings import MAX_STEPS

def guard_node(state, llm_output):
    state.step_count += 1

    if state.step_count >= MAX_STEPS:
        llm_output["next_action"]["instruction_to_user"] += (
            "\nWe will pause here to avoid overload."
        )

    if llm_output["internal_assessment"]["needs_emergency_support"]:
        state.emergency_triggered = True

    state.last_assessment = llm_output
    state.history.append(llm_output)

    return state
