import os
from google.adk.apps import App
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from google.adk.models.google_llm import Gemini
from tools import get_local_menu, search_menu_vector

# Note: For use when Agent Platform is easier to configure
#gemini_model = Gemini(
#    model="gemini-flash-latest",
#    project="[REPLACE_YOUR_GCP_PROJECT_ID_HERE]",
#    location=os.environ.get("REGION", "us-central1")
#)

# --- Specialists ---
brew_master_agent = LlmAgent(
    name="BrewMasterAgent",
    model="gemini-3.8-flash",
    description="Artisan extraction and brewing expert. Provides grind size, brew ratios, water temp, and pouring guides.",
    instruction="""
    You are an expert coffee brewing consultant.
    When asked about whole beans or home extraction:
      1. Recommend grind size (e.g., medium-fine for V60, coarse for French Press).
      2. Provide coffee-to-water ratio (e.g., 1:16).
      3. Recommend water temperature (e.g., 93°C / 200°F).
      4. Give a concise step-by-step pouring schedule.
    """,
)
brew_master_tool = AgentTool(agent=brew_master_agent)

# --- Coordinator ---
barista_agent = LlmAgent(
    name="BaristaCoordinator",
    model="gemini-3.8-flash",
    instruction="""
    You are the barista concierge at the artisan coffee counter.
    - Always verify item availability and prices using your menu tools.
    - If a customer mentions an allergy, check ingredients and warn them.
    - If a customer asks how to brew whole beans at home, delegate to the `BrewMasterAgent`.
    - Be friendly, efficient, and concise.
    """,
    tools=[get_local_menu]  # Update as you progress through steps
)

# Export the App object for InMemoryRunner
app = App(
    name="coffee_barista_app",
    root_agent=barista_agent
)
