# Prompt Log
Project: HRHelper – HR FAQ Chatbot (Web + Slack Integration)
Initial Goal

Build an HR FAQ chatbot that works in two ways:

Web UI – where employees can ask HR-related questions.

Slack bot – where the bot can respond when mentioned in Slack.

Key Development Steps
1. Core Functionality

Created faqs.json with predefined HR-related questions and answers.

Used RapidFuzz to implement fuzzy matching so the bot can understand similar questions.

Set a matching threshold (40%) to improve flexible question matching.

Implemented a fallback message if no relevant answer is found.

2. FastAPI Backend

Created / route to serve the chatbot page using Jinja2 templates.

Created /ask route to handle user input from the web UI.

Created /slack/events route to:

Handle Slack’s url_verification challenge.

Listen for app_mention events.

Send replies using slack_sdk’s chat.postMessage.

3. Slack Bot Integration

Generated Slack Bot Token and Signing Secret from Slack API dashboard.

Stored them securely in .env file and loaded them using python-dotenv.

Verified bot authentication with auth_test() method.

Configured Event Subscriptions in Slack to point to the ngrok URL for /slack/events.

Subscribed to the app_mention event so the bot responds when tagged.

4. Web UI (chat.html)

Styled the chat interface with light pink and blue gradients.

Added a suggested questions section with clickable FAQ buttons.

Added user and bot avatars to chat bubbles.

Implemented "HRHelper is typing..." animation before responses appear.

Updated layout to be more rectangular and clean.

5. Debugging & Fixes

Fixed path issues for loading faqs.json (app/data/faqs.json).

Solved "invalid_auth" Slack error by loading correct token from .env.

Fixed issue where bot responded the same to all questions by lowering fuzzy match threshold.

Corrected send button JavaScript so it works in the updated UI.
