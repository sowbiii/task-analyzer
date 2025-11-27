from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_priority_score

class ScoringTests(TestCase):

    def test_overdue_task_high_score(self):
        task = {
            "title": "Overdue",
            "due_date": date.today() - timedelta(days=2),
            "estimated_hours": 2,
            "importance": 5,
            "dependencies": []
        }
        score, explanation = calculate_priority_score(task, mode="smart")
        self.assertTrue(score > 10)  # overdue should push score up

    def test_low_effort_fastest_mode(self):
        task = {
            "title": "Quick win",
            "due_date": date.today() + timedelta(days=10),
            "estimated_hours": 0.5,
            "importance": 3,
            "dependencies": []
        }
        score, explanation = calculate_priority_score(task, mode="fastest")
        self.assertTrue(score > 3)  # low effort should have reasonable score

    def test_impact_mode_prefers_importance(self):
        task = {
            "title": "Important",
            "due_date": date.today() + timedelta(days=5),
            "estimated_hours": 8,
            "importance": 9,
            "dependencies": []
        }
        score_impact, _ = calculate_priority_score(task, mode="impact")
        score_smart, _ = calculate_priority_score(task, mode="smart")
        self.assertTrue(score_impact >= score_smart)
