# AI ERPNext Business Assistant

An AI-powered business assistant that connects to **ERPNext** and uses **LangGraph Reflection and Reflexion** to analyze, review, and improve customer-specific sales-order responses.

## Architecture

```text
User Request
     ↓
Customer
     ↓
Sales Order Service
     ↓
Customer-wise ERPNext Data
     ↓
LangGraph State
     ↓
Analyzer
     ↓
Reflector
     ↓
Conditional Routing
   ↙              ↘
Approved       Not Approved
   ↓                ↓
  END            Feedback
                    ↓
                  Lesson
                    ↓
            Previous Attempts
                    ↓
                 Analyzer
                    ↓
                Reflector
```

The workflow can repeat until the response is approved or the maximum iteration limit is reached.

## Key Features

* ERPNext REST API integration
* Customer-wise sales-order retrieval
* LLM-based sales-order analysis
* LangGraph Reflection workflow
* Reflexion using feedback, lessons, and previous attempts
* Conditional routing and retry loop
* Maximum iteration control
* Deterministic order-count validation using Python
* FastAPI API layer
* Gradio comparison UI
* Live LangGraph node execution in Gradio
* LangSmith tracing and observability
* Local LLM inference with Ollama

## Customer-wise Sales Order Retrieval

The assistant retrieves sales orders for the requested customer instead of fetching orders from all customers.

For example:

```text
Customer: Sandeep
        ↓
ERPNext Sales Order API
        ↓
Filter: customer = Sandeep
        ↓
Only Sandeep's Sales Orders
```

This ensures that the Analyzer receives only the relevant customer's sales-order data.

## Reflection

The **Analyzer** generates the sales-order summary.

The **Reflector** reviews the generated response against the verified ERPNext order data and deterministic order counts.

It checks:

* Total Orders
* Completed Orders
* Pending Orders
* Cancelled Orders
* Whether Draft orders are correctly included in Pending Orders

If the response is not approved, LangGraph routes the workflow through the improvement process.

```text
Generate
   ↓
Review
   ↓
Decide
   ↓
Retry / Terminate
```

### Reflection Demo

Screenshot showing the Reflection workflow.

<img width="1512" height="883" alt="Reflection workflow" src="https://github.com/user-attachments/assets/43733d76-b632-42d4-8824-a2fb49d8bd93" />

## Reflexion

Reflexion extends the Reflection workflow by using information from previous attempts to improve the next attempt.

The workflow stores:

* Previous answer
* Critique
* Feedback
* Lesson

The next Analyzer attempt receives the lesson and previous attempts as additional context.

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

A simple list in the LangGraph state is used to store previous attempts. No vector database or long-term memory is used for this implementation.

### Reflexion Demo

Screenshot showing the Reflexion workflow.

<img width="1521" height="791" alt="image" src="https://github.com/user-attachments/assets/9d7c65e4-5b2c-475a-90b3-6ea24e292348" />


## Live Workflow Streaming

The Gradio interface uses LangGraph workflow streaming to display node execution while the Reflexion workflow is running.

Example:

```text
Starting Reflexion workflow...

✓ analyzer
✓ reflector
✓ feedback
✓ lesson

✓ analyzer
✓ reflector

✓ Workflow completed
```

The exact number of iterations depends on whether the Reflector approves the generated response or requests another attempt.

This makes the execution of the LangGraph workflow visible instead of waiting only for the final response.

The streaming flow is:

```text
workflow.stream()
       ↓
Analyzer
       ↓
Reflector
       ↓
Conditional Routing
       ↓
Feedback / END
       ↓
Lesson
       ↓
Analyzer
       ↓
...
```

### Live Workflow Demo

<img width="1521" height="791" alt="image" src="https://github.com/user-attachments/assets/44d5e153-e406-4e16-9166-7080bfa2933b" />


## LangSmith Observability

The project uses **LangSmith** for tracing and observability of the LangGraph workflow.

LangSmith helps inspect:

* Workflow execution
* LLM calls
* Node execution
* Inputs and outputs
* Multiple Reflexion iterations
* Execution traces

The application loads LangSmith configuration from environment variables:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=<your-api-key>
LANGSMITH_PROJECT=ai-erpnext-assistant
```

The API key is stored in `.env` and is not committed to the repository.

```text
Gradio
   ↓
LangGraph Workflow
   ↓
Analyzer → Reflector → Feedback → Lesson
   ↓
LangSmith Traces
```

LangSmith provides observability into the workflow, while LangGraph is responsible for executing the workflow and conditional routing.

## Deterministic Validation

Order counts are calculated using Python from the current ERPNext sales-order data instead of relying on the LLM to calculate them.

For example:

```text
ERPNext Data
    ↓
Python
    ↓
Verified Order Counts
    ↓
LangGraph State
    ↓
Analyzer / Reflector
```

This helps prevent the LLM from incorrectly interpreting similar ERPNext statuses such as:

```text
To Deliver

To Deliver and Bill
```

The application treats these ERPNext statuses as distinct statuses, while mapping the relevant statuses to the business-level Pending Orders count:

```text
To Deliver
To Bill
To Deliver and Bill
Draft
```

Draft orders are included in the Pending Orders count for the assistant's business-level summary.

## Gradio Demo

The Gradio UI compares the same customer-specific sales-order analysis:

```text
┌─────────────────────┬────────────────────────┐
│ Without Reflexion   │ With Reflexion         │
│                     │                        │
│ Customer            │ Customer               │
│    ↓                │    ↓                   │
│ Analyzer            │ Analyzer               │
│    ↓                │    ↓                   │
│ First Answer        │ Reflector              │
│                     │    ↓                   │
│                     │ Feedback               │
│                     │    ↓                   │
│                     │ Lesson                 │
│                     │    ↓                   │
│                     │ Analyzer Again         │
│                     │    ↓                   │
│                     │ Final Answer           │
└─────────────────────┴────────────────────────┘
```

The comparison demonstrates the difference between a direct LLM response and a response processed through the Reflexion workflow.

The **With Reflexion** workflow also displays live node execution while the graph is running.

## Reliability Note

During testing, the local LLM could still produce factual inconsistencies in some responses.

The project therefore separates deterministic business logic from LLM-generated reasoning:

* Python handles verified order counts.
* The LLM handles analysis and explanation.
* Reflector reviews the generated response.
* Reflexion provides feedback, lesson generation, and retry.
* LangGraph controls workflow execution and routing.
* LangSmith provides workflow observability and tracing.

Reflexion improves the review and retry process but does not guarantee factual correctness.

Future improvements will include broader automated evaluation and additional reliability checks.

## Tech Stack

**Python · FastAPI · LangGraph · LangChain · LangSmith · Ollama · Qwen 2.5 3B · ERPNext · Gradio**

## Project Structure

```text
ai-erpnext-assistant/

├── app/
│   ├── agents/
│   ├── api/
│   ├── erpnext/
│   └── graph/
├── data/
├── tests/
├── main.py
└── requirements.txt
```

## Current Status

* [x] ERPNext integration
* [x] Customer-wise sales-order retrieval
* [x] Analyzer
* [x] Reflection
* [x] Reflexion
* [x] Feedback and lesson loop
* [x] Previous-attempt tracking
* [x] Conditional routing
* [x] Retry loop
* [x] Maximum iteration control
* [x] Deterministic order-count validation
* [x] Gradio UI
* [x] Live LangGraph workflow streaming
* [x] LangSmith tracing and observability
* [ ] Multi-Agent
* [ ] Multi-Graph / Subgraphs
* [ ] Evaluation
