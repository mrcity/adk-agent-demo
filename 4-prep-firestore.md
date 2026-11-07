# Deploy a RAG AI Agent in Streamlit using Google ADK and Cloud Run

## 4. Ground your agent in Firestore using Vector Search

### Preface

Because this can take a long time, let's take time now to set up the indexes and other cloud infrastructure. Then, we can run the app locally and mess with it while the index builds, and then simply switch out the agent tool when the index is done.

In a production scenario, storing your menu items in a local `menu.json` file is not ideal because any change to the menu requires rebuilding the container image and redeploying the Cloud Run service.

To make the application dynamic and scalable, you can migrate your menu data to **Cloud Firestore** and use **Vector Search** to retrieve only the most relevant menu items based on semantic similarity.

![Integrating Firestore Using Vector Search](https://codelabs.developers.google.com/static/codelabs/cloud-run/build-streamlit-rag-agent-google-adk-cloud-run/images/integrating-firestore.png)

### 1. Enable the Firestore API and Initialize Database
Run the following commands to enable the Firestore API and create a Firestore database named coffee-menu in Native mode:

```
gcloud services enable firestore.googleapis.com
gcloud firestore databases create --database="coffee-menu" --location=$REGION
```

Note: API enablement can take 1–2 minutes to propagate. If the database creation command prompts you with `API [firestore.googleapis.com] not enabled on project... Would you like to enable and retry?`, type `Y` to proceed, or wait a minute and rerun the command.

### 2. Seed Firestore with the Menu Data
To quickly seed your Firestore database with the menu items from your menu.json file, you can run a Python script locally in Cloud Shell.

1. Install the Firestore and GenAI client libraries locally in Cloud Shell to run the seeding script:

```
pip3 install google-cloud-firestore==2.27.0 google-genai==2.11.0
```

2. Study the script `seed.py` to see how it utilizes a text embedding model to encode the menu data into the vector store.

3. Run the script:

```
python3 seed.py
```

### 3. Create Firestore Vector Index

To perform vector searches on your menu items, you must create a composite vector index on the `embedding` field in your Firestore database.

Run the following command in the Cloud Shell terminal:

```
gcloud firestore indexes composite create \
 --collection-group=menu \
 --query-scope=COLLECTION \
 --database="coffee-menu" \
 --field-config=field-path=embedding,vector-config='{"dimension":"768", "flat": "{}"}'
```
Note: Firestore index creation runs in the background and can take a few minutes to complete. You can proceed with the next steps of the codelab while the index is building.

### 4. Grant Firestore Access to the Service Account

For your Cloud Run service to query Firestore, you must grant its service account the **Cloud Datastore User** (`roles/datastore.user`) role:

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
 --member="serviceAccount:barista-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
 --role="roles/datastore.user"
```
Note: Although we are using Cloud Firestore in Native mode, Google Cloud utilizes the unified Cloud Datastore IAM roles (roles/datastore.viewer or roles/datastore.user) to manage access control.