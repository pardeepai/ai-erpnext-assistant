# AI ERPNext Business Assistant

An AI-powered business assistant that connects to **ERPNext** and uses **LangGraph Reflection, Reflexion, and Multi-Agent workflows** to analyze and respond to customer-specific business queries.

---

## Architecture

The project has evolved through multiple LangGraph patterns:

```text
Reflection
    ↓
Reflexion
    ↓
Multi-Agent
    ↓
Multi-Graph / Subgraphs
    ↓
Evaluation
```

The current implementation includes Reflection, Reflexion, and Multi-Agent workflows.

---

## Key Features

* ERPNext REST API integration
* Customer-wise sales-order retrieval
* Customer information retrieval
* Customer contact information retrieval
* LLM-based sales-order analysis
* LangGraph Reflection workflow
* Reflexion using feedback, lessons, and previous attempts
* Customer Supervisor Agent
* Customer Details Agent
* Customer Contact Agent
* Conditional Multi-Agent routing
* Customer details and contact data separation
* Combined final response generation
* Conditional routing and retry loop
* Maximum iteration control
* Deterministic order-count validation using Python
* FastAPI API layer
* Gradio comparison UI
* Live LangGraph node execution in Gradio
* LangSmith tracing and observability
* Local LLM inference with Ollama

---

# Reflection and Reflexion Workflow

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

---

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

---

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

<img width="1521" height="791" alt="Reflexion workflow" src="https://github.com/user-attachments/assets/9d7c65e4-5b2c-475a-90b3-6ea24e292348" />

---

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

<img width="1521" height="791" alt="Live workflow" src="https://github.com/user-attachments/assets/44d5e153-e406-4e16-9166-7080bfa2933b" />

---

# Multi-Agent Workflow

The project extends the Reflexion-based assistant with a customer-focused **Multi-Agent workflow**.

Instead of using one agent to handle every customer request, the system uses specialized agents for different types of customer information.

```text
User Request
     ↓
Customer Name Extraction
     ↓
Customer Supervisor
     ↓
Route Decision
   ↙    ↓     ↘
Details Contact Both
   ↓      ↓      ↓
Details Contact Details
Agent    Agent    Agent
                  ↓
             Contact Agent
   ↓      ↓       ↓
   └──────┴───────┘
           ↓
    Final Response
```

The Multi-Agent workflow currently supports three routes:

```text
details
contact
both
```

---

## Customer Name Extraction

The workflow first identifies the customer mentioned in the user's request.

For example:

```text
Show me sandeep customer group
              ↓
        Customer: sandeep
```

```text
Show me sandeep phone number
              ↓
        Customer: sandeep
```

The extracted customer name is then used by the ERPNext services to retrieve the required data.

---

## Customer Supervisor Agent

The **Customer Supervisor Agent** is responsible for deciding which customer specialist should handle the request.

Available routes:

### `details`

Used for customer information such as:

* Customer name
* Customer type
* Customer group
* Territory
* General customer information

### `contact`

Used for contact information such as:

* Phone number
* Email
* Mobile number

### `both`

Used when the request requires information from both customer details and contact information.

The Supervisor only performs routing. It does not answer the user's question.

```text
User Request
     ↓
Supervisor
     ↓
Route
 ┌───────┬─────────┬───────┐
 ↓       ↓         ↓
details contact   both
```

---

## Customer Details Agent

The **Customer Details Agent** handles customer-related information retrieved from ERPNext.

It can work with information such as:

* Customer name
* Customer type
* Customer group
* Territory
* General customer information

The ERPNext API/service layer retrieves the customer data before it is passed to the agent.

The agent itself does not directly perform ERPNext API calls.

---

## Customer Contact Agent

The **Customer Contact Agent** handles customer contact information.

It works with:

* Phone number
* Email address
* Mobile number

The contact information is retrieved through the ERPNext contact service before being passed to the agent.

This keeps ERPNext API access separated from agent logic.

---

## Multi-Agent Routing

The LangGraph workflow uses conditional routing to select the required specialist.

### Details Route

```text
User Request
     ↓
Customer Name
     ↓
Supervisor
     ↓
Details Route
     ↓
Details Agent
     ↓
Final Response
```

### Contact Route

```text
User Request
     ↓
Customer Name
     ↓
Supervisor
     ↓
Contact Route
     ↓
Contact Agent
     ↓
Final Response
```

### Both Route

```text
User Request
     ↓
Customer Name
     ↓
Supervisor
     ↓
Both Route
     ↓
Details Agent
     ↓
Contact Agent
     ↓
Final Response
```

The `both` route intentionally executes the Details Agent first and then the Contact Agent before reaching the common Final Response node.

---

## Final Response

The **Final Response node** is shared by all routes.

It combines the required structured data retrieved from ERPNext based on the selected route.

For example:

```text
Details Route
     ↓
customer_details
     ↓
Final Response
```

```text
Contact Route
     ↓
customer_contact
     ↓
Final Response
```

```text
Both Route
     ↓
customer_details + customer_contact
     ↓
Final Response
```

This approach avoids blindly concatenating specialist-agent responses.

For example, the Customer Details API may not contain a phone number while the Contact API does. The Final Response node therefore uses the appropriate source for each field.

---

## Multi-Agent Examples

### Details Query

```text
Query:

Show me sandeep customer group

Route:

details

Flow:

Customer Name
     ↓
Supervisor
     ↓
Details Agent
     ↓
Final Response
```

Example result:

```text
Customer Information:

- Customer Name: sandeep
- Customer Type: Company
- Customer Group: Commercial
```

---

### Contact Query

```text
Query:

Show me sandeep phone number

Route:

contact

Flow:

Customer Name
     ↓
Supervisor
     ↓
Contact Agent
     ↓
Final Response
```

Example result:

```text
Customer Information:

- Customer Name: sandeep
- Phone Number: 890887
- Email Address: pdddsaws@example.com
```

---

### Both Query

```text
Query:

Show me sandeep customer group and phone number

Route:

both

Flow:

Customer Name
     ↓
Supervisor
     ↓
Details Agent
     ↓
Contact Agent
     ↓
Final Response
```

Example result:

```text
Customer Information:

- Customer Name: sandeep
- Customer Type: Company
- Customer Group: Commercial
- Phone Number: 890887
- Email Address: pdddsaws@example.com
```

---

# LangSmith Observability

The project uses **LangSmith** for tracing and observability of the LangGraph workflows.

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

For the Multi-Agent workflow:

```text
Gradio
   ↓
LangGraph
   ↓
Supervisor
   ↓
Details / Contact / Both
   ↓
Specialist Agents
   ↓
Final Response
   ↓
LangSmith Trace
```

LangSmith provides observability into the workflow, while LangGraph is responsible for executing the workflow and conditional routing.

---

# Deterministic Validation

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

---

# Gradio Demo

The Gradio UI originally compares the same customer-specific sales-order analysis:

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

The current Gradio application also supports the Multi-Agent workflow:

```text
User Query
    ↓
Customer Name
    ↓
Supervisor
    ↓
Specialist Agent
    ↓
Final Response
```

---

# Reliability Note

During testing, the local LLM could still produce factual inconsistencies in some responses.

The project therefore separates deterministic business logic from LLM-generated reasoning:

* Python handles verified order counts.
* ERPNext services handle data retrieval.
* The LLM handles analysis and explanation.
* Specialist agents handle domain-specific customer information.
* The Supervisor handles Multi-Agent routing.
* The Final Response node combines structured data.
* Reflector reviews the generated response.
* Reflexion provides feedback, lesson generation, and retry.
* LangGraph controls workflow execution and routing.
* LangSmith provides workflow observability and tracing.

Reflexion improves the review and retry process but does not guarantee factual correctness.

Similarly, Multi-Agent routing separates responsibilities between specialized agents but does not by itself guarantee factual correctness.

Future improvements will include broader automated evaluation and additional reliability checks.

---

# Tech Stack

**Python · FastAPI · LangGraph · LangChain · LangSmith · Ollama · Qwen 2.5 3B · ERPNext · Gradio**

---

# Project Structure

```text
ai-erpnext-assistant/

├── app/
│   ├── agents/
│   │   ├── customer_supervisor.py
│   │   ├── customer_details.py
│   │   └── customer_contact.py
│   │
│   ├── api/
│   │
│   ├── erpnext/
│   │   ├── client.py
│   │   ├── customer.py
│   │   ├── contact.py
│   │   └── sales_order.py
│   │
│   └── graph/
│       ├── state.py
│       ├── nodes.py
│       ├── edges.py
│       ├── prompts.py
│       ├── workflow.py
│       └── workflow_multi.py
│
├── data/
├── tests/
│   ├── test_supervisor.py
│   └── ...
│
├── main.py
├── multi_agent_gradio_app.py
└── requirements.txt
```

---

# Current Status

## Core ERPNext + Reflection/Reflexion

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

## Multi-Agent

* [x] Customer name extraction
* [x] Customer Supervisor Agent
* [x] Customer Details Agent
* [x] Customer Contact Agent
* [x] Details routing
* [x] Contact routing
* [x] Both routing
* [x] ERPNext customer details service
* [x] ERPNext contact service
* [x] Common Final Response node
* [x] Route-specific final response handling
* [x] Tested details route
* [x] Tested contact route
* [x] Tested both route
* [x] Multi-Agent

## Upcoming

* [ ] Multi-Graph / Subgraphs
* [ ] Evaluation

---

# Development Approach

The project is developed incrementally rather than building a large agent system at once.

Each milestone focuses on understanding the architecture, implementing it, testing it, and debugging failures.

The development approach is:

```text
Understand
    ↓
Build
    ↓
Test
    ↓
Break
    ↓
Debug
    ↓
Explain
    ↓
Move to Next Milestone
```

This helps ensure that each LangGraph concept is understood before introducing the next architectural pattern.

---

# Future Roadmap

```text
[x] Reflection
      ↓
[x] Reflexion
      ↓
[x] Multi-Agent
      ↓
[ ] Multi-Graph / Subgraphs
      ↓
[ ] Evaluation
```

Future improvements may include:

* Multi-Graph / Subgraph architecture
* Automated evaluation
* Response quality metrics
* Routing evaluation
* Reliability testing
* Additional ERPNext business capabilities
* More specialized business agents
* Improved production observability