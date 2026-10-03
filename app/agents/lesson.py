from langchain_ollama import ChatOllama


class LessonAgent:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0,
        )

    def generate_lesson(self, reflection, feedback):
        prompt = f"""
You are a lesson agent.

Based on the reflection and feedback below, create
one short reusable rule that the Analyzer should remember
for future attempts.

Reflection:
{reflection}

Feedback:
{feedback}

Create a lesson that:
- captures the actual mistake
- states the correct rule
- can be reused in future attempts
- does not focus on formatting unless formatting was the actual problem
- does not invent new information

Give only the short lesson.
"""

        response = self.llm.invoke(prompt)

        return response.content.strip()