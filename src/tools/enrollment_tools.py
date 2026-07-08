"""
Enrollment Tools
=================
Defines the three tools that the Student Enrollment Agent can call:
    1. get_program_info     - Retrieve program details
    2. check_application_status - Check applicant status by ID
    3. get_deadlines        - Retrieve program deadlines

Each tool queries the mock data store and returns a dictionary.
"""

import logging

from langchain_core.tools import tool

from src.tools.mock_data import APPLICANTS, DEADLINES, PROGRAMS

logger = logging.getLogger(__name__)


def _get_available_programs() -> str:
    """Return a comma-separated string of all available program names."""
    return ", ".join(program["program_name"] for program in PROGRAMS.values())


@tool
def get_program_info(program_name: str) -> dict:
    """Retrieve information about a university program including duration, tuition, and prerequisites.

    Args:
        program_name: Name of the program to look up (case-insensitive).

    Returns:
        Dictionary containing program_name, duration, tuition, and prerequisites.
    """
    key = program_name.lower().strip()
    logger.info("Looking up program info for: '%s'", key)

    if key in PROGRAMS:
        return PROGRAMS[key]

    logger.warning("Program '%s' not found in database", program_name)
    return {
        "error": f"Program '{program_name}' not found. "
        f"Available programs: {_get_available_programs()}"
    }


@tool
def check_application_status(applicant_id: str) -> dict:
    """Check the application status of a prospective student using their applicant ID.

    Args:
        applicant_id: Unique applicant identifier (e.g., 'APP-1042').

    Returns:
        Dictionary containing applicant_name, program_applied, status, and next_step.
    """
    key = applicant_id.upper().strip()
    logger.info("Checking application status for ID: '%s'", key)

    if key in APPLICANTS:
        return APPLICANTS[key]

    logger.warning("Applicant ID '%s' not found in database", applicant_id)
    return {
        "error": f"Applicant ID '{applicant_id}' not found. "
        "Please verify your ID and try again."
    }


@tool
def get_deadlines(program_name: str) -> dict:
    """Retrieve important deadlines for a specific program.

    Returns application deadline, document submission deadline,
    and decision notification date.

    Args:
        program_name: Name of the program to look up (case-insensitive).

    Returns:
        Dictionary containing program deadlines.
    """
    key = program_name.lower().strip()
    logger.info("Looking up deadlines for program: '%s'", key)

    if key in DEADLINES:
        return DEADLINES[key]

    logger.warning("Deadlines for program '%s' not found", program_name)
    return {
        "error": f"Program '{program_name}' not found. "
        f"Available programs: {_get_available_programs()}"
    }
