"""
Mock Data Store
================
Contains hardcoded mock data simulating the university's database
for programs, applicants, and deadlines.

In a production environment, these would be replaced with actual
database queries or API calls.
"""

from typing import Final


# ─────────────────────────────────────────────
# Program Information
# ─────────────────────────────────────────────

PROGRAMS: Final[dict[str, dict]] = {
    "computer science": {
        "program_name": "Computer Science",
        "duration": "4 years",
        "tuition": "$40,000/year",
        "prerequisites": ["Mathematics", "Physics", "English Proficiency"],
    },
    "data science": {
        "program_name": "Data Science",
        "duration": "2 years (Master's)",
        "tuition": "$35,000/year",
        "prerequisites": ["Statistics", "Linear Algebra", "Programming Fundamentals"],
    },
    "business administration": {
        "program_name": "Business Administration",
        "duration": "4 years",
        "tuition": "$38,000/year",
        "prerequisites": ["Mathematics", "English Proficiency"],
    },
}

# ─────────────────────────────────────────────
# Applicant Records
# ─────────────────────────────────────────────

APPLICANTS: Final[dict[str, dict]] = {
    "APP-1042": {
        "applicant_name": "Alice Johnson",
        "program_applied": "Computer Science",
        "status": "Documents Pending",
        "next_step": "Submit official transcripts and letter of recommendation.",
    },
    "APP-2085": {
        "applicant_name": "Bob Smith",
        "program_applied": "Data Science",
        "status": "Under Review",
        "next_step": "Wait for the review committee's decision by March 15, 2026.",
    },
    "APP-3071": {
        "applicant_name": "Carol Davis",
        "program_applied": "Business Administration",
        "status": "Accepted",
        "next_step": "Confirm enrollment and pay the deposit by April 1, 2026.",
    },
}

# ─────────────────────────────────────────────
# Program Deadlines
# ─────────────────────────────────────────────

DEADLINES: Final[dict[str, dict]] = {
    "computer science": {
        "program_name": "Computer Science",
        "application_deadline": "March 1, 2026",
        "document_submission_deadline": "March 15, 2026",
        "decision_notification_date": "April 10, 2026",
    },
    "data science": {
        "program_name": "Data Science",
        "application_deadline": "February 15, 2026",
        "document_submission_deadline": "March 1, 2026",
        "decision_notification_date": "March 30, 2026",
    },
    "business administration": {
        "program_name": "Business Administration",
        "application_deadline": "April 1, 2026",
        "document_submission_deadline": "April 15, 2026",
        "decision_notification_date": "May 10, 2026",
    },
}
