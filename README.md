# AI ERPNext Business Assistant

An AI-powered business assistant that connects to ERPNext and uses LangGraph workflows to analyze customer-specific business queries.

## Overview

This project implements:

- ERPNext REST API integration
- Customer-wise sales-order retrieval
- Customer details and contact retrieval
- LLM-based sales-order analysis
- Reflection workflow
- Reflexion workflow with feedback and lesson loop
- Customer Supervisor, Details, and Contact agents
- Conditional multi-agent routing
- Final response generation
- LangSmith tracing
- Gradio UI for workflow demos

## Architecture

```text
Reflection
    ↓
Reflexion
    ↓
Multi-Agent
    ↓
Final Response
```

The current implementation includes Reflection, Reflexion, and Multi-Agent workflows.

## Reflection and Reflexion Workflow

### Customer-wise Sales Order Retrieval

The assistant retrieves sales orders for the requested customer instead of fetching all orders.

```text
Customer: Sandeep
        ↓
ERPNext Sales Order API
        ↓
Filter: customer = Sandeep
        ↓
Only Sandeep's Sales Orders
```

### Reflection

The Analyzer generates the sales-order summary. The Reflector reviews the result against ERPNext order data and deterministic order counts.

It checks:

- Total Orders
- Completed Orders
- Pending Orders
- Cancelled Orders
- Draft orders included in Pending Orders

If the response is not approved, the workflow retries.

### Reflexion

Reflexion extends Reflection by storing previous attempts, feedback, and lessons and reusing them in the next try.

```text
Attempt
    ↓
Reflection
    ↓
Feedback
    ↓
Lesson
    ↓
Store Previous Attempt
    ↓
Next Attempt
```

## Multi-Agent Workflow

The project also includes a customer-focused multi-agent workflow.

```text
User Request
      ↓
Customer Name Extraction
      ↓
Customer Supervisor
      ↓
Route Decision
    ↙    ↓     ↘
 details  contact  both
    ↓      ↓      ↓
Details Agent Contact Agent Final Response
```

### Routes

- `details`: customer details such as customer type and group
- `contact`: customer phone/email information
- `both`: combined details and contact data

The Final Response node combines the correct data from the selected route.

## LangSmith Observability

The project uses LangSmith to trace workflow execution and monitor node runs.

## Deterministic Validation

Order counts are calculated using Python from ERPNext sales-order data, then used to validate the LLM-generated summary.

## Gradio Demo

The project includes Gradio-based demos for the workflow comparison and multi-agent flow.

## Tech Stack

- Python
- FastAPI
- LangGraph
- LangChain
- LangSmith
- Ollama
- Qwen 2.5 3B
- ERPNext
- Gradio

## Project Structure

```text
ai-erpnext-assistant/

├── app/
│   ├── agents/
│   │   ├── customer_supervisor.py
│   │   ├── customer_details.py
│   │   └── customer_contact.py
│   ├── api/
│   ├── erpnext/
│   │   ├── client.py
│   │   ├── customer.py
│   │   ├── contact.py
│   │   └── sales_order.py
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   ├── edges.py
│   │   ├── prompts.py
│   │   ├── workflow.py
│   │   └── workflow_multi.py
│   └── gradio_app.py
├── data/
├── tests/
│   ├── test_supervisor.py
│   └── ...
├── main.py
├── multi_agent_gradio_app.py
├── requirements.txt
└── README.md
```

## Current Status

### Core ERPNext + Reflection/Reflexion

- [x] ERPNext integration
- [x] Customer-wise sales-order retrieval
- [x] Analyzer
- [x] Reflection
- [x] Reflexion
- [x] Feedback and lesson loop
- [x] Previous-attempt tracking
- [x] Conditional routing
- [x] Retry loop
- [x] Maximum iteration control
- [x] Deterministic order-count validation
- [x] Gradio UI
- [x] Live LangGraph workflow streaming
- [x] LangSmith tracing and observability

### Multi-Agent

- [x] Customer name extraction
- [x] Customer Supervisor Agent
- [x] Customer Details Agent
- [x] Customer Contact Agent
- [x] Details routing
- [x] Contact routing
- [x] Both routing
- [x] ERPNext customer details service
- [x] ERPNext contact service
- [x] Common Final Response node
- [x] Route-specific final response handling
- [x] Tested details route
- [x] Tested contact route
- [x] Tested both route
- [x] Multi-Agent

## How to Run

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the FastAPI app:

```bash
uvicorn main:app --reload
```

4. To run the Gradio demos, use the provided app entry points in the project.

## Notes

The project separates business validation logic from LLM-generated reasoning:

- Python handles deterministic order counts.
- ERPNext services handle data retrieval.
- The LLM handles analysis and explanation.
- Supervisor and specialist agents handle customer routing and domain-specific responses.
- Reflector and Reflexion improve the answer quality through review and retry.
