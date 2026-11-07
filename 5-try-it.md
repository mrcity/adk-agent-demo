# Deploy a RAG AI Agent in Streamlit using Google ADK and Cloud Run

## 5. Try the basic version running the menu locally

While we wait for the Firestore to initialize, let's at least run the Streamlit application and see what we've built so far, and take it for a spin.

### Instantiate Streamlit

1. Open up a new cloud terminal instance.

2. Start the Streamlit server.

```
streamlit run app.py --server.port 8080 --server.enableCORS false --serve
r.enableXsrfProtection false
```

### Test the RAG behavior

Open the Cloud Run service URL in a web browser and ask the AI Barista questions to test its grounding and safety constraints.

In-menu request: Ask: "Recommend something strong and warm."Expected: The agent recommends Espresso.
Out-of-menu trap: Ask: "Do you have a matcha frappuccino?"Expected: The agent politely declines and explains it is not on the menu.
Allergen-aware request: Ask: "I'm lactose intolerant, what can I get?"Expected: The agent only recommends dairy-free menu items (like Oat Milk Latte, Espresso, Cold Brew). It does NOT recommend Cappuccino or Croissant.

Open the Cloud Run service URL in a web browser and ask the AI Barista questions to test its grounding and safety constraints.

1. **In-menu request:** Ask: _"Recommend something strong and warm."_ Expected: The agent recommends Espresso.
2. **Out-of-menu trap:** Ask: _"Do you have a matcha frappuccino?"_ Expected: The agent politely declines and explains it is not on the menu.
3. **Allergen-aware request:** Ask: _"I'm lactose intolerant, what can I get?"_ Expected: The agent only recommends dairy-free menu items (like Oat Milk Latte, Espresso, Cold Brew). It does NOT recommend Cappuccino or Croissant.

![Testing the RAG Behavior](https://codelabs.developers.google.com/static/codelabs/cloud-run/build-streamlit-rag-agent-google-adk-cloud-run/images/testing.png)