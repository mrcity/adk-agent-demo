# Deploy a RAG AI Agent in Streamlit using Google ADK and Cloud Run

## 1. Introduction
In this codelab, you will build an interactive **AI Barista agent** for a specialty coffee shop. Using Google's open-source **Agent Development Kit (ADK)** and the **Gemini 3.8 Flash** model, you will implement **Retrieval-Augmented Generation (RAG)** to ground the agent's recommendations in a menu dataset containing pricing, allergens, and whole-bean roast profiles.

Finally, you will wrap the agent in a **Streamlit** conversational user interface and run it live using Google Cloud Shell Web Preview.

### Architecture Overview

### What you'll learn
* How to initialize and configure a Google Cloud project with Google AI Studio, Vertex AI, and Cloud Run APIs.
* How to construct an agent with Google's Agent Development Kit (ADK) using `LlmAgent`.
* How to implement tool grounding (RAG) using Python function tools.
* How to interface ADK's `InMemoryRunner` with a Streamlit chat front-end.
* How browser session state (`st.session_state`) interacts with backend agent memory.

### Prerequisites
* Access to Google Cloud Platform.
* A modern web browser (Google Chrome recommended).
* Basic familiarity with Python and terminal commands.


