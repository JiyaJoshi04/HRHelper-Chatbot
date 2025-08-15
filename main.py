import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from rapidfuzz import fuzz
from fastapi.staticfiles import StaticFiles



# Load environment variables
load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET")

print("DEBUG TOKEN:", slack_token)
print("DEBUG SIGNING SECRET:", slack_signing_secret)

slack_client = WebClient(token=slack_token)
signature_verifier = SignatureVerifier(signing_secret=slack_signing_secret)

# Test Slack auth
try:
    resp = slack_client.auth_test()
    print("Slack auth test:", resp)
except Exception as e:
    print("Slack auth failed:", e)

# Load FAQs
faq_file_path = Path(__file__).parent / "data" / "faqs.json"
faq_file_path = faq_file_path.resolve()
with open(faq_file_path, "r", encoding="utf-8") as f:
    faqs = json.load(f)
print("✅ FAQs loaded:", faqs)

# Find answer function
def find_answer(user_question: str) -> str:
    best_match = None
    highest_score = 0
    for faq in faqs:
        score = fuzz.ratio(user_question.lower(), faq["question"].lower())
        if score > highest_score:
            highest_score = score
            best_match = faq
    if best_match and highest_score >= 60:
        return best_match["answer"]
    return "I'm sorry, I don't have an answer for that. Please contact HR."

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "faqs": faqs})


# Endpoint for web chatbot
@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")
    answer = find_answer(question)
    return {"question": question, "answer": answer}

# Endpoint for Slack events
@app.post("/slack/events")
async def slack_events(request: Request):
    raw_body = await request.body()
    data = json.loads(raw_body)

    if data.get("type") == "url_verification":
        return PlainTextResponse(content=data.get("challenge"))

    if "event" in data:
        event = data["event"]
        if event.get("type") == "app_mention":
            text = re.sub(r"<@[^>]+>\s*", "", event.get("text", "")).strip()
            answer = find_answer(text)
            slack_client.chat_postMessage(channel=event["channel"], text=answer)

    return JSONResponse(content={"ok": True})
