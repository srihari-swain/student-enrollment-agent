# Student Enrollment Assistant — Test Conversation Output

## Test Configuration
- **Model:** gpt-4o-mini
- **Framework:** LangChain + LangGraph
- **Agent:** create_agent (ReAct pattern)

---

## Turn 1

**User:** Hi, what programs do you offer in computer science?

**Tool Called:** `get_program_info(program_name="computer science")`

**Agent:** We offer a Bachelor's degree in Computer Science. Here are the details:

- **Duration:** 4 years
- **Tuition:** $40,000 per year
- **Prerequisites:** You should have a background in Mathematics, Physics, and English Proficiency.

If you have any more questions or need information about other programs, feel free to ask!

---

## Turn 2

**User:** What's the application deadline for that?

**Tool Called:** `get_deadlines(program_name="computer science")` *(remembered from Turn 1)*

**Agent:** The application deadlines for the Computer Science program are as follows:

- **Application Deadline:** March 1, 2026
- **Document Submission Deadline:** March 15, 2026
- **Decision Notification Date:** April 10, 2026

If you need any more information or assistance, just let me know!

---

## Turn 3

**User:** I already applied. My ID is APP-1042. What's my status?

**Tool Called:** `check_application_status(applicant_id="APP-1042")`

**Agent:** Hello, Alice Johnson! Here's the status of your application for the Computer Science program:

- **Status:** Documents Pending
- **Next Step:** Please submit your official transcripts and letter of recommendation.

If you have any further questions or need assistance, feel free to ask!

---

## Turn 4

**User:** Can I get a fee waiver?

**Tool Called:** *None (escalated — outside tool capabilities)*

**Agent:** I'd recommend speaking with an enrollment counselor for that. Would you like me to connect you?

---

## Turn 5

**User:** What documents do I still need to submit?

**Tool Called:** *None (used context from Turn 3 — remembered applicant status)*

**Agent:** You still need to submit the following documents for your application:

- **Official Transcripts**
- **Letter of Recommendation**

If you have any other questions or need further assistance, feel free to ask!

---

## Summary

| Turn | User Question | Tool Used | Behavior |
|------|--------------|-----------|----------|
| 1 | Programs in computer science? | `get_program_info` | Tool call — returned program details |
| 2 | Application deadline for that? | `get_deadlines` | Multi-turn context — remembered "computer science" |
| 3 | My ID is APP-1042, status? | `check_application_status` | Tool call — returned applicant status |
| 4 | Can I get a fee waiver? | None | Graceful escalation — outside tool scope |
| 5 | What documents do I need? | None | Multi-turn context — used Turn 3 results |
