from langchain_ollama import ChatOllama


class FeedbackAgent:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0,
        )

    def generate_feedback(self, reflection):
        prompt = f"""
You are a feedback agent.

The Reflector reviewed the previous analysis and identified a problem.

Reflection:
{reflection}

Your task:
Convert the reflection into a clear correction instruction
for the Analyzer's next attempt.

The instruction should explain:
- what was wrong
- what the Analyzer should do differently
- what rule should be followed

Do not invent new information.
Do not focus on formatting unless the reflection specifically
identifies a formatting problem.

Give only the correction instruction.
"""

        response = self.llm.invoke(prompt)

        return response.content.strip()