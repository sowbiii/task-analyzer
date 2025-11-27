from datetime import date

def calculate_priority_score(task, mode="smart"):
    today = date.today()

    # Urgency calculation
    if task["due_date"] is None:
        urgency = 0
    else:
        days_left = (task["due_date"] - today).days
        if days_left < 0:
            urgency = 10  # overdue
        elif days_left == 0:
            urgency = 9
        else:
            urgency = max(1, 10 - days_left)

    importance = task.get("importance", 1)
    effort = task.get("estimated_hours", 1)
    dependency_count = len(task.get("dependencies", []))

    # Different modes
    if mode == "fastest":
        score = (10 / (effort + 1)) + importance
        explanation = "Prioritized because it requires low effort."

    elif mode == "impact":
        score = importance * 2 + urgency
        explanation = "High-impact task with strong importance score."

    elif mode == "deadline":
        score = urgency * 2 + importance
        explanation = "Prioritized due to urgent deadline."

    else:  # SMART BALANCED
        score = (
            (importance * 1.5) +
            (urgency * 1.3) +
            (10 / (effort + 1)) +
            (dependency_count * 2)
        )
        explanation = "Balanced score using importance, urgency, effort, and dependencies."

    return round(score, 2), explanation
