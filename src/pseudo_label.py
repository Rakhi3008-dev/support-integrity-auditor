priority_map = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4
}

def infer_severity(score, q1, q2, q3):

    if score < q1:
        return "Low"

    elif score < q2:
        return "Medium"

    elif score < q3:
        return "High"

    else:
        return "Critical"

def severity_delta(assigned, inferred):

    return (
        priority_map[inferred]
        - priority_map[assigned]
    )

def mismatch_label(delta):
    return int(abs(delta) >= 2)

def mismatch_type(delta):

    if delta >= 2:
        return "Hidden Crisis"

    elif delta <= -2:
        return "False Alarm"

    return "Consistent"