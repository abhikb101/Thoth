import os
import re
import sys
from threading import Thread

from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
import logging
from settings import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, SLACK_SIGNING_SECRET, OPENAI_API_KEY
from gpt import chatgpt_refresh
from handlers.events import handle_mention, handle_summary, handle_ask_thoth

logging.basicConfig(level=logging.DEBUG)

oauth_settings = OAuthSettings(
    client_id=SLACK_CLIENT_ID,
    client_secret=SLACK_CLIENT_SECRET,
    scopes=["channels:read", "groups:read", "chat:write", "app_mentions:read","incoming-webhook"],
    installation_store=FileInstallationStore(base_dir="./data/installations"),
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="./data/states")
)

app = App(signing_secret=SLACK_SIGNING_SECRET,
    oauth_settings=oauth_settings,
    logger=logging.getLogger('tcpserver'))


@app.event("app_mention")
def app_mention(event, say):
    response = handle_mention(event)
    say(response['response'], thread_ts=response['thread_ts'])

@app.event("message")
def app_message(event, say):
    response = handle_mention(event)
    say(response['response'], thread_ts=response['thread_ts'])

@app.message("summarize this")
def summary_this(event, say):
    handle_summary(event, say)

@app.message("create jira")
def create_jira(event, say):
    resp=handle_jira(event)
    say(send, thread_ts=event.get("thread_ts") or event.get("ts"))

@app.message("ask thoth")
def ask_thoth(event, say):
    handle_ask_thoth(event, say)

@app.message("knock knock")
def ask_who(message, say):
    say("_Who's there?_")

if __name__ == "__main__":
    print("Bot Started!", file=sys.stderr)
    thread = Thread(target=chatgpt_refresh)
    thread.start()
    app.start(4000)  # POST http://localhost:4000/slack/events
