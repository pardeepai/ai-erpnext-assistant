from dotenv import load_dotenv

# Load environment variables before importing workflow/LLM components
load_dotenv()

import gradio as gr

from app.graph.workflow_multi import workflow


def run_multi_agent(user_query):
    initial_state = {
        "user_query": user_query,
        "customer_name": None,
        "customer_details": {},
        "customer_contact": {},
        "route": "",
        "contact_response": "",
        "details_response": "",
        "final_response": "",
    }

    final_state = workflow.invoke(initial_state)

    return final_state["final_response"]


with gr.Blocks() as demo:

    gr.Markdown("# ERPNext AI Multi-Agent Assistant")

    user_query = gr.Textbox(
        label="User Query",
        placeholder="Example: Show me sandeep customer group and phone number",
        lines=3,
    )

    run_button = gr.Button("Run Query")

    final_output = gr.Textbox(
        label="Final Response",
        lines=15,
        max_lines=25,
    )

    run_button.click(
        fn=run_multi_agent,
        inputs=user_query,
        outputs=final_output,
    )


demo.launch()