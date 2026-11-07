# Deploy a RAG AI Agent in Streamlit using Google ADK and Cloud Run

## 7. Deploy the agent to Cloud Run

You will deploy the Streamlit application directly from source using Cloud Run's built-in buildpacks. To follow the principle of least privilege, you will create and deploy using a dedicated custom service account rather than using the default Compute Engine service account.

1. Create a dedicated service account:

```
  gcloud iam service-accounts create barista-agent-sa \
    --description="Service account for Coffee Barista ADK agent on Cloud Run" \
    --display-name="Barista Agent Service Account"
```

2. Grant the Gemini Enterprise Agent Platform user role (`roles/aiplatform.user`) to the new service account:

```
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:barista-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

3. Deploy the service using `gcloud run deploy`, passing the new service account email via the `--service-account` flag:

```
gcloud run deploy coffee-barista \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --labels dev-tutorial=codelab-streamlit-rag-adk \
  --command "/cnb/lifecycle/launcher" \
  --args "sh,-c,python3 -m streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false" \
  --service-account "barista-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --set-env-vars GOOGLE_GENAI_USE_ENTERPRISE=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=global
```

> Note: If prompted to create an Artifact Registry Docker repository to store built containers (e.g., `Do you want to continue (Y/n)?`), type `Y` to continue. The initial source deployment builds the container in the cloud. This step usually takes 3-5 minutes to complete.

4. Once deployed, locate the service URL in the command output.

### 💬 Discussion: Deploying Containers vs. Source, and IAM Security

**We deployed to Cloud Run using gcloud run deploy –source without creating a Dockerfile or a Procfile. How did Cloud Run figure out how to compile and execute our Python app?**

Cloud Run uses Buildpacks under the hood to analyze your repository. Upon detecting the presence of `requirements.txt` and Python source files, the engine automatically compiles and packages a Python runtime container.

Writing a custom `Dockerfile` gives you complete control over your container's system packages and base layers. A `Procfile` is a simpler way to declare the startup command without fully configuring a container. But for quick deployments, deploying from source (`--source`) is highly efficient.

**Why did we go through the extra step of creating a custom service account barista-agent-sa instead of just using the default Compute Engine service account?**

Safety first! The default Compute Engine service account has extremely broad Editor permissions by default. Running our Cloud Run container under the default service account means if our app has a security bug, an attacker could potentially read, write, or delete other resources in our Google Cloud project.

By creating a dedicated service account and only assigning it the `roles/aiplatform.user` role, we follow the Principle of Least Privilege: the app has exactly the access it needs to call Gemini, and nothing more.