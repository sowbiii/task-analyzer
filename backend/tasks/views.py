from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from .scoring import calculate_priority_score
from .serializers import TaskSerializer

# POST /api/tasks/analyze/
@api_view(["POST"])
def analyze_tasks(request):
    tasks = request.data.get("tasks", [])
    mode = request.data.get("mode", "smart")

    if not isinstance(tasks, list):
        return Response({"error": "Tasks must be a list"}, status=status.HTTP_400_BAD_REQUEST)

    scored_tasks = []

    for task in tasks:
        # Convert due date if needed
        if isinstance(task.get("due_date"), str):
            try:
                task["due_date"] = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            except:
                task["due_date"] = None

        score, explanation = calculate_priority_score(task, mode)
        task["score"] = score
        task["explanation"] = explanation

        scored_tasks.append(task)

    # Sort by score (descending)
    scored_tasks = sorted(scored_tasks, key=lambda x: x["score"], reverse=True)

    return Response({"tasks": scored_tasks}, status=200)


# GET /api/tasks/suggest/
@api_view(["GET"])
def suggest_tasks(request):
    tasks = request.GET.get("tasks")

    if not tasks:
        return Response({"error": "Tasks parameter required"}, status=400)

    import json
    tasks = json.loads(tasks)

    suggestions = []

    for task in tasks:
        if isinstance(task.get("due_date"), str):
            try:
                task["due_date"] = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            except:
                task["due_date"] = None

        score, explanation = calculate_priority_score(task, "smart")
        task["score"] = score
        task["explanation"] = explanation
        suggestions.append(task)

    suggestions = sorted(suggestions, key=lambda x: x["score"], reverse=True)[:3]

    return Response({"top_tasks": suggestions})
