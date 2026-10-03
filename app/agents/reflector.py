from langchain_ollama import ChatOllama


class SalesOrderReflector:

  def __init__(self):
    self.llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0,
    )

  def reflect(
      self,
      analysis: str,
      sales_orders: dict,
      order_counts: dict,
  ):
    prompt = f"""
You are a strict fact-checking reviewer for a sales order assistant.

ACTUAL SALES ORDER DATA:
{sales_orders}

VERIFIED ORDER COUNTS:
{order_counts}

ANALYSIS TO REVIEW:
{analysis}

BUSINESS RULES:

- Total Orders = order_counts["total"]
- Completed Orders = order_counts["completed"]
- Pending Orders = order_counts["pending"] + order_counts["draft"]
- Cancelled Orders = order_counts["cancelled"]

STATUS DEFINITIONS:

- Completed = "Completed"
- Pending = "To Deliver", "To Bill", "To Deliver and Bill", or "Draft"
- Cancelled = "Cancelled"

CHECK THE ANALYSIS:

1. Check whether Total Orders is correct.
2. Check whether Completed Orders is correct.
3. Check whether Pending Orders correctly includes Draft orders.
4. Check whether Cancelled Orders is correct.

IMPORTANT:
Do NOT require a "- Draft Orders: 0" line.
Focus on whether the actual numbers are correct.

If any number is incorrect:
APPROVED: False
REFLECTION: Explain which number is incorrect and what the correct number should be.

If all numbers are correct:
APPROVED: True
REFLECTION: The order counts are correct.

Return ONLY:
APPROVED: True or False
REFLECTION: <short explanation>
"""
    response = self.llm.invoke(prompt)
    content = response.content.strip()
    approved = "APPROVED: True" in content
    reflection = (
        content.replace("APPROVED: True", "")
        .replace("APPROVED: False", "")
        .replace("REFLECTION:", "")
        .strip()
    )

    return {
        "reflection": reflection,
        "approved": approved,
    }