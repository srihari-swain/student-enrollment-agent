"""
Student Enrollment Agent
=========================
Implements a conversational AI agent for university admissions
using LangChain's create_agent.

The agent follows the ReAct (Reasoning + Acting) pattern:
    1. Reason about the user's question.
    2. Decide which tool(s) to call (if any).
    3. Observe the tool results.
    4. Formulate a natural language response.

The agent maintains conversation history across turns using
LangGraph's InMemorySaver checkpointer, enabling multi-turn
context awareness (e.g., remembering applicant IDs).
"""

import logging

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from src.tools.enrollment_tools import check_application_status, get_deadlines, get_program_info

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a Student Enrollment Assistant at a university admissions office.

Your role is to help prospective students by answering their questions about:
- Academic programs (details, tuition, duration, prerequisites)
- Application deadlines (submission dates, decision notification dates)
- Application status (current status, next steps)

You have access to the following tools:
1. **get_program_info** — Retrieves details about a specific program (name, duration, tuition, prerequisites).
2. **get_deadlines** — Retrieves important dates for a program (application deadline, document deadline, decision date).
3. **check_application_status** — Looks up an applicant's status using their unique applicant ID.

## How to Approach Questions

Think step-by-step before responding:
1. Identify what the user is asking about.
2. Determine if any of your tools can provide the answer.
3. If yes, call the appropriate tool with the correct input. Always prefer calling a tool over asking clarifying questions.
4. Use the tool's response to craft a helpful, natural answer.

When a user mentions a program name or asks about offerings in a field, always call get_program_info \
to retrieve its details. Never escalate program-related questions — use the tool first.

## Important Rules
- ALWAYS call a tool before responding if the question relates to programs, deadlines, or application status.
- Only escalate to a counselor for topics completely unrelated to your tools (fee waivers, scholarships, housing, etc.).

## Context Awareness

Pay attention to the full conversation history. If the user previously mentioned a program name \
or applicant ID, use that context — do not ask them to repeat information they have already provided.

## Escalation

If the user asks about something outside your tools' capabilities \
(e.g., fee waivers, scholarships, housing, financial aid, campus tours), \
respond with: "I'd recommend speaking with an enrollment counselor for that. \
Would you like me to connect you?"

Always be friendly, concise, and helpful in your responses."""

# Thread ID for maintaining conversation state
THREAD_ID = "enrollment_session_1"

class StudentEnrollmentAgent:
    """Conversational agent for university admissions using LangChain's create_agent.

    This agent uses the ReAct pattern to:
        - Reason about user queries and decide which tools to call.
        - Execute tools and formulate natural language responses.
        - Maintain conversation history via InMemorySaver checkpointer.
        - Gracefully escalate when questions fall outside tool capabilities.

    Attributes:
        tools: List of available LangChain tools.
        llm: ChatOpenAI instance for language model inference.
        agent: Compiled LangChain agent with memory.
        config: Agent invocation config with thread_id for session tracking.

    Example:
        >>> agent = StudentEnrollmentAgent(openai_api_key="sk-...")
        >>> response = agent.chat("What programs do you offer?")
        >>> print(response)
    """

    def __init__(self, openai_api_key: str, model: str) -> None:
        """Initialize the enrollment agent.

        Args:
            openai_api_key: Valid OpenAI API key for authentication.
            model: OpenAI model identifier to use. Defaults to gpt-4o-mini.
        """
        logger.info("Initializing StudentEnrollmentAgent with model: %s", model)

        self.tools = [get_program_info, check_application_status, get_deadlines]

        self.llm = ChatOpenAI(
            model=model,
            api_key=openai_api_key,
        )

        # Create agent using LangChain's create_agent with memory checkpointer
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
            checkpointer=InMemorySaver(),
        )

        # Config with thread_id enables multi-turn conversation memory
        self.config = {"configurable": {"thread_id": THREAD_ID}}

    def chat(self, user_input: str) -> str:
        """Process a single user turn and return the agent's response.

        The agent reasons about the input, decides whether to call tools,
        executes them if needed, and returns a natural language response.
        Conversation history is automatically maintained via the checkpointer.

        Args:
            user_input: The user's natural language message.

        Returns:
            The agent's natural language response string.
        """
        logger.info("User input: %s", user_input)

        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=self.config,
        )

        response = result["messages"][-1].content
        logger.info("Agent response: %s", response[:100])
        return response

    def reset(self) -> None:
        """Clear conversation history by creating a new checkpointer.

        This effectively starts a fresh session while keeping
        the same agent configuration.
        """
        logger.info("Resetting conversation history")
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
            checkpointer=InMemorySaver(),
        )
