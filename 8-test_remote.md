# Deploy a RAG AI Agent in Streamlit using Google ADK and Cloud Run

## 8. Verify the Firestore Integration on the Remote App

To test the agent's connection to Firestore, add a brand-new menu item directly in Firestore and verify that the agent recommends it.

1. Run the following command in Cloud Shell to write a new document to the `menu` collection in Firestore using Python:

```
python3 -c "
import os
from google import genai
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector

db = firestore.Client(database='coffee-menu')
client = genai.Client(
   vertexai=True,
   project=os.environ.get('PROJECT_ID'),
   location=os.environ.get('REGION', 'us-central1')
)

name = 'Matcha Green Tea Latte'
desc = 'Creamy steamed oat milk infused with premium Japanese matcha powder.'
res = client.models.embed_content(
   model='text-embedding-005',
   contents=f'{name}: {desc}'
)
embedding = res.embeddings[0].values

db.collection('menu').document('matcha-latte').set({
   'name': name,
   'description': desc,
   'price': 5.50,
   'tags': ['sweet', 'hot', 'dairy-free'],
   'allergens': [],
   'embedding': Vector(embedding)
})
print('Successfully added Matcha Latte with vector embeddings!')
"
```

2. Refresh your Streamlit app in the browser to clear the chat session and load the new database state.

3. Notice that:
  * **Matcha Green Tea Latte** automatically appears in the sidebar menu.
  * Ask the chatbot: _"Do you have any matcha drinks?"_
  * The agent should successfully recommend the new **Matcha Green Tea Latte** with the description and price you just added. This confirms the agent is query-grounded directly in your live Firestore database!
ls
