"""
Main Entry Point
==================
Runs the Student Enrollment Assistant Agent through a 5-turn
test conversation as specified in the assignment requirements.

Usage:
    export OPENAI_API_KEY="your-key-here"
    python main.py
"""

import logging
import os
import sys

from dotenv import load_dotenv

from src.agent.enrollment_agent import StudentEnrollmentAgent

load_dotenv()

# ─────────────────────────────────────────────
# Logging Configuration
# ─────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Test Conversation
# ─────────────────────────────────────────────

TEST_MESSAGES: list[str] = [
    "Hi, what programs do you offer in computer science?",
    "What's the application deadline for that?",
    "I already applied. My ID is APP-1042. What's my status?",
    "Can I get a fee waiver?",
    "What documents do I still need to submit?",
]


def run_test_conversation() -> None:
    """Run the 5-turn test conversation and print the full input/output log.

    Reads the OpenAI API key from the OPENAI_API_KEY environment variable.
    If not set, prompts the user for input.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API key: ").strip()
        if not api_key:
            logger.error("No API key provided. Exiting.")
            sys.exit(1)

    model = os.environ.get("MODEL_NAME", "gpt-4o-mini")
    agent = StudentEnrollmentAgent(openai_api_key=api_key, model=model)

    print("=" * 60)
    print("   Student Enrollment Assistant - Test Conversation")
    print("=" * 60)

    for turn_number, user_msg in enumerate(TEST_MESSAGES, start=1):
        print(f"\n{'─' * 40}")
        print(f"  Turn {turn_number}")
        print(f"{'─' * 40}")
        print(f"  User:  {user_msg}")

        response = agent.chat(user_msg)
        print(f"  Agent: {response}")

    print(f"\n{'=' * 60}")
    print("   Test Conversation Complete")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    run_test_conversation()
