# Deploy a RAG AI Agent in Streamlit using Google ADK and Cloud Run

## 3. Review project files

Rather than copying them into your workspace, let's just review them here.

### menu.json - A quick & dirty way to give the AI some context

To ground the AI Barista and prevent it from hallucinating non-existent items, we provide a local menu dataset at [menu.json](menu.json). The agent will read this file at runtime via a custom tool.

#### Discussion: Local JSON vs. Live Databases

Why are we using a simple local menu.json file instead of a live database?

For a quick tutorial or prototype, a local JSON file eliminates initial database setup time and complexity. However, in a real-world enterprise production application, you would connect the agent to a managed database like Cloud Firestore, AlloyDB, or Cloud SQL.

Using a live database allows coffee shop managers to add seasonal items, update prices, or adjust allergen tags dynamically without rebuilding the container image or redeploying the application code. We will be using a live database as an optional step later in the codelab.

### [agent.py](agent.py) - The overall behavior of the agents, and ADK scaffolding

### [tools.py](tools.py) - Actions and specific routines that agents can call upon to refine answers

### [app.py](app.py) - Serve the chatbot through a Streamlit interface

#### 💬 Discussion: Model Tradeoffs & Retrieval Token Efficiency

**Why call a function tool to retrieve the menu instead of just pasting the entire menu text into the agent's system instructions?**

Token economy! Putting 8 items in the prompt is cheap, but what if the coffee shop expands to 500 items, including custom ingredients? Pasting large datasets directly into the system prompt inflates your prompt token count, increasing transaction costs and API response latency on every single query.

By using an ADK tool, the agent dynamically asks to read the menu ONLY when needed. The LLM only receives the relevant menu data as context, minimizing the prompt token size.

#### 💬 Discussion: Memory State & Production Stores

**Does the chat history stored inside Streamlit's st.session_state persist when a user closes their browser tab?**

No, it doesn't. `st.session_state` is completely in-memory and unique to the active browser connection. If a user refreshes the page or closes the tab, their conversation history with the barista is lost.

For a production application, you would connect the ADK runner to a persistent storage backend like Cloud Firestore or Redis. ADK provides built-in service abstractions (like `SessionService`) that make it simple to save and resume chat history across page reloads and devices.

