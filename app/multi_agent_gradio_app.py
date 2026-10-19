
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

    final_state = initial_state.copy()
    progress_messages = []

    try:
        for event in workflow.stream(initial_state):
            for node_name, node_update in event.items():
                progress_messages.append(
                    f"Completed node: {node_name}"
                )

                # Merge each node's state updates.
                final_state.update(node_update)
                print("STREAM EVENT:", node_name, repr(node_update))
                
                print("Final state after node execution:", final_state)
                # Show execution progress in the Gradio interface.
                yield (
                    "\n".join(progress_messages),
                    final_state.get("final_response", "")
                )

        # Return the final response after all nodes finish.
        yield (
            "\n".join(progress_messages) + "\n\nWorkflow completed.",
            final_state.get("final_response", "")
        )
        print("Final state after workflow execution:", final_state)

    except Exception:
        # Log the technical exception on the server, not in the UI.
        import logging
        logging.exception("Multi-agent workflow execution failed")

        yield (
            "\n".join(progress_messages)
            + "\n\nWorkflow failed. Check the application logs.",
            "Unable to complete the request. Please try again later."
        )


with gr.Blocks() as demo:
    gr.Markdown("# ERPNext AI Multi-Agent Assistant")

    user_query = gr.Textbox(
        label="User Query",
        placeholder="Example: Show me Sandeep's customer group and phone number",
        lines=3,
    )

    run_button = gr.Button("Run Query")
    

    with gr.Row():
        progress_output = gr.Textbox(
            label="Workflow Progress",
            lines=10,
            interactive=False,
        )

        final_output = gr.Textbox(
            label="Final Response",
            lines=15,
            max_lines=25,
            interactive=False,
        )

    run_button.click(
        fn=run_multi_agent,
        inputs=user_query,
        outputs=[progress_output, final_output],
    )

print("After button.click")
demo.queue()
demo.launch()
