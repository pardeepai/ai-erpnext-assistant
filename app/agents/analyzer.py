from langchain_ollama import ChatOllama


class SalesOrderAnalyzer:

  def __init__(self):
    self.llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0,
    )

  def analyze(
      self,
      customer,
      orders,
      order_counts,
      feedback="",
      lesson="",
      previous_attempts=None,
  ):
    # Check if feedback or lesson is present from attempt 1
    has_feedback_or_lesson = bool(
        (feedback and feedback.strip()) or (lesson and lesson.strip())
    )
    
    if has_feedback_or_lesson:
        attempt_rule = """
RETRY ATTEMPT:

Feedback and lesson are available from the previous attempt.

Apply the feedback and lesson.

For this attempt, calculate Pending Orders correctly:

Pending Orders = order_counts["pending"] + order_counts["draft"]

The correct Pending Orders count is 3.
"""
    else:
        attempt_rule = """
FIRST ATTEMPT — DELIBERATE ERROR FOR REFLEXION EXERCISE:

For this first attempt only, intentionally make the Pending Orders
calculation incorrect.

Use:

Pending Orders = order_counts["pending"]

Do NOT add order_counts["draft"].

This should produce Pending Orders = 2.

This mistake is intentional so that the Reflector can detect it.
"""

    prompt = f"""
You are a sales order assistant.

Analyze the CURRENT sales order data and provide a simple,
customer-friendly summary.

Customer:
{customer}

CURRENT ORDERS:
{orders}

VERIFIED ORDER COUNTS:
{order_counts}

FEEDBACK FROM PREVIOUS REVIEW:
{feedback}

LESSON FROM PREVIOUS ATTEMPT:
{lesson}

PREVIOUS ATTEMPTS:
{previous_attempts}

{attempt_rule}

Output:
- Total Orders
- Completed Orders
- Pending Orders
- Cancelled Orders
- A short observation

IMPORTANT:

The VERIFIED ORDER COUNTS were calculated by Python
from the CURRENT ORDERS.

Correct business rules:

- Total Orders = order_counts["total"]
- Completed Orders = order_counts["completed"]
- Pending Orders = order_counts["pending"] + order_counts["draft"]
- Cancelled Orders = order_counts["cancelled"]

STATUS DEFINITIONS:

- Completed = "Completed"
- Pending = "To Deliver", "To Bill", "To Deliver and Bill", or "Draft"
- Cancelled = "Cancelled"

CURRENT ORDERS and VERIFIED ORDER COUNTS are the source of truth.

Feedback, lesson, and previous attempts may help improve
the response, but must not override the current data.

Do not invent information.
"""

    response = self.llm.invoke(prompt)

    return response.content