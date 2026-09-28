from dotenv import load_dotenv

# Load environment variables before importing the workflow/LLM components
load_dotenv()

import gradio as gr

from app.erpnext.sales_order import SalesOrderService
from app.agents.analyzer import SalesOrderAnalyzer
from app.graph.workflow import workflow


sales_order_service = SalesOrderService()
analyzer = SalesOrderAnalyzer()


# WITHOUT REFLEXION
def analyze_without_reflexion(customer):
    orders = sales_order_service.get_sales_orders(customer)

    order_counts = sales_order_service.get_order_counts(orders)

    analysis = analyzer.analyze(
        customer=customer,
        orders=orders,
        order_counts=order_counts,
    )

    return analysis


# WITH REFLEXION
def analyze_with_reflexion(customer):
    orders = sales_order_service.get_sales_orders(customer)

    order_counts = sales_order_service.get_order_counts(orders)

    initial_state = {
        "customer": customer,
        "sales_orders": orders,
        "order_counts": order_counts,
        "analysis": "",
        "reflection": "",
        "approved": False,
        "iteration": 0,
        "feedback": "",
        "lesson": "",
        "previous_attempts": [],
    }

    workflow_status = "Starting Reflexion workflow...\n"

    final_state = initial_state

    # Stream the LangGraph workflow node by node
    for event in workflow.stream(initial_state):

        for node_name, node_state in event.items():

            workflow_status += f"✓ {node_name}\n"

            final_state = node_state

            # Update the workflow status in Gradio
            yield workflow_status, final_state.get("analysis", "")

    workflow_status += "✓ Workflow completed\n"

    yield workflow_status, final_state["analysis"]


with gr.Blocks() as demo:

    gr.Markdown("# ERPNext AI Business Assistant")

    customer = gr.Textbox(
        label="Customer",
        placeholder="Enter customer name",
    )

    analyze_button = gr.Button("Analyze Customer")

    with gr.Row():

        # WITHOUT REFLEXION
        with gr.Column():

            gr.Markdown("### Without Reflexion")

            output_without = gr.Textbox(
                label="Analyzer Output",
                lines=25,
                max_lines=30,
            )

        # WITH REFLEXION
        with gr.Column():

            gr.Markdown("### With Reflexion")

            workflow_status = gr.Textbox(
                label="Live Workflow",
                lines=10,
                max_lines=15,
            )

            output_with = gr.Textbox(
                label="Final Output",
                lines=15,
                max_lines=25,
            )

    # Without Reflexion
    analyze_button.click(
        fn=analyze_without_reflexion,
        inputs=customer,
        outputs=output_without,
    )

    # With Reflexion
    analyze_button.click(
        fn=analyze_with_reflexion,
        inputs=customer,
        outputs=[workflow_status, output_with],
    )


demo.launch()