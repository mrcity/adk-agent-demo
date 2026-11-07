# Deploy a RAG AI Agent in Streamlit using Google ADK and Cloud Run

## 2. Project setup

### Create a Google Cloud Project

1. In the [Google Cloud Console](https://console.cloud.google.com/), on the project selector page, select or create a Google Cloud project.
2. Make sure that billing is enabled for your Cloud project. Learn how to [confirm billing is enabled on a project](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled).

**Billing Required:** You must have an active billing account linked to your project to enable Vertex AI APIs and deploy services to Cloud Run.

### Activate Cloud Shell

You will perform all development and deployment operations from **Cloud Shell**, a free browser-based command line environment preloaded with the Google Cloud CLI (`gcloud`), Python, and Git.

1. In the upper-right corner of the Google Cloud console, click **Activate Cloud Shell** (terminal icon).

![the Cloud Shell icon in the toolbar](https://codelabs.developers.google.com/static/codelabs/cloud-run/build-streamlit-rag-agent-google-adk-cloud-run/images/activate-cloud-shell.png)

2. Confirm your authentication:

![Click the Authorize button to authorize Cloud Shell](https://codelabs.developers.google.com/static/codelabs/cloud-run/build-streamlit-rag-agent-google-adk-cloud-run/images/authorize-cloud-shell.png)

And run `gcloud auth list`

3. Confirm your active project is set:

```
gcloud config get project
```

If the project ID shown is not correct or none is set, run:

```
gcloud config set project <YOUR_PROJECT_ID>
```

### Enable APIs

Run this command to enable all the required APIs:

```
gcloud services enable \
 run.googleapis.com \
 aiplatform.googleapis.com \
 cloudbuild.googleapis.com
```

> Verification Tip: API activation typically takes 2 to 3 minutes. You can verify that they are ready by running gcloud services list --enabled and checking that both run.googleapis.com, aiplatform.googleapis.com and cloudbuild.googleapis.com appear in the output

### Get a Gemini API key

Get the API key from [Google AI Studio](https://aistudio.google.com).

Stash your Gemini API key as an environment variable:

```
export GEMINI_API_KEY=AQ...etc...
```

#### Note to Enterprise users looking for better governance
Another alternative is to use Gemini Agent Platform and its application-default credentials. This is the "Get a Gemini API Key" button shown at the front page of the GCP Console. But, for prototyping purposes, getting the API key from AI Studio works effectively.

### Initialize shell and working directory

In this step, you will initialize your project environment variables and create a working directory for your project.

1. In your active Cloud Shell session, initialize the following project environment variables:

```
export PROJECT_ID=$(gcloud config get-value project)
```

Find your closest region and replace `insert-region-here` with it in the following command:

```
export REGION=[insert-region-here]
# In NA, use us-central1
```

2. Clone this repository:

```
git clone https://github.com/mrcity/adk-agent-demo
```

3. Install Python dependencies

Change into the codelab directory:

```
cd adk-agent-demo
```

The dependencies are already called out in `requirements.txt`, so simply install the requirements like this:

```
pip install -r requirements.txt
```

