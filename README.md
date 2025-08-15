# HRHelper-Chatbot
#HRHelper – Employee FAQ Chatbot

HRHelper is a FastAPI-based chatbot that answers HR-related FAQs from a JSON dataset.  
It supports both **a web UI** and **Slack integration**, allowing employees to get answers instantly.

##  Features
- Web-based chatbot with a modern UI.
- Slack bot that responds to mentions.
- Fuzzy string matching to handle different question formats.
- Suggested FAQs for quick access.
- Easy to update – just edit `faqs.json`.
- Real-time responses in Slack and browser.

Create Virtual Environment & Install Dependencies
python -m venv venv
venv\Scripts\activate        

pip install -r requirements.txt

Setup Environment Variables
Create a .env file in the root folder:
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token

SLACK_SIGNING_SECRET=your-slack-signing-secret

Running the App
Web UI
uvicorn app.main:app --reload

Slack Integration Setup
Create a Slack App in Slack API.

Bot Token Scopes: app_mentions:read, chat:write, commands

Event Subscriptions → Subscribe to app_mention.

Set Request URL to your public ngrok URL + /slack/events.

Install the app to your workspace.

Invite the bot to a Slack channel:/invite @HRHelper



