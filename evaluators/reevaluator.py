def needs_reevaluation(assessment):
    return (
        assessment["confidence_in_previous_step"] < 0.4
        or assessment["needs_reevaluation"]
    )
