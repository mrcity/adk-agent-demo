# Deploy a RAG AI Agent in Streamlit using Google ADK and Cloud Run

## 6. Finish adding Firestore

Now that the Firestore index should be built, let's update the code to actually take advantage of it, retrieving the menu from Firestore instead of reading from menu.json.

### Change the agent

The change to the agent is simple. All you need to do is change

```
    tools=[get_local_menu]
```

to 

```
    tools=[search_menu_vector]
```