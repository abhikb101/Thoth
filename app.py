import os
import re
import sys
import time
from threading import Thread
import re
from revChatGPT.V3 import Chatbot
from slack_bolt import App
from dotenv import load_dotenv
from funcs import get_all_messages, summarize_data, get_user_by_id
from jira import JIRA

pattern = r"<@[A-Z\d]+>"

load_dotenv()
ChatGPTConfig = {
    "api_key": os.getenv("OPENAI_API_KEY"),
}
JiraApiKey = os.getenv("JIRA_API_KEY")
jiraOptions = {'server': "https://venlabs.atlassian.net/"}
JiraEmail = os.getenv("JIRA_EMAIL")

jira = JIRA(options=jiraOptions, basic_auth=(JiraEmail, JiraApiKey))

issue_dict = {
    'project': {'key': 'VEN'},
    'summary': '',
    'description': '',
    'issuetype': {'name': 'Bug'},
}

if os.getenv("OPENAI_ENGINE"):
    ChatGPTConfig["engine"] = os.getenv("OPENAI_ENGINE")

app = App()
chatbot = Chatbot(**ChatGPTConfig)

def create_jira(prompt):
    issue_dict['summary'] = prompt
    issue_dict['description'] = prompt
    new_issue = jira.create_issue(fields=issue_dict)

def is_jira_issue_intent(prompt):
    if "jira" in prompt.lower():
        return True
    return False

def handle_event(event, say, is_mention):
    prompt = re.sub("\\s<@[^, ]*|^<@[^, ]*", "", event["text"])

    # Each thread should be a separate conversation
    convo_id = event.get("thread_ts") or event.get("ts") or ""

    try:
        response = chatbot.ask(prompt, convo_id=convo_id)
        user = event["user"]

        if is_mention:
            send = f"<@{user}> {response}"
        else:
            send = response
    except Exception as e:
        print(e, file=sys.stderr)
        send = "We are experiencing exceptionally high demand. Please, try again."

    if is_mention:
        # Get the `ts` value of the original message
        original_message_ts = event["ts"]
    else:
        original_message_ts = None

    # Use the `app.event` method to send a message
    say(send, thread_ts=original_message_ts)


@app.event("app_mention")
def handle_mention(event, say):
    if "analyze this" in event['text'].lower():
        splitted = event['text'].split("/")
        channel_id = splitted[4]
        thread_ts = splitted[-1].split("?")[1].split("&")[0].split("=")[1]
        get_all_messages(thread_ts, channel_id)
        return
    
    if "summarize this" in event['text'].lower():
        splitted = event['text'].split("/")
        channel_id = splitted[4]
        thread_ts = splitted[-1].split("?")[1].split("&")[0].split("=")[1]
        resp = summarize_data(thread_ts, channel_id)
        say(resp, thread_ts=event.get("thread_ts") or event.get("ts"))
        return
        
    if is_jira_issue_intent(event['text']):
        create_jira(event['text'])
        send = "It's done"
        say(send, thread_ts=event.get("thread_ts") or event.get("ts"))
        print(is_jira_issue_intent(event['text']), file=sys.stderr)
        return

    handle_event(event, say, is_mention=True)


@app.event("message")
def handle_message(event, say):
    print(event, say)

def chatgpt_refresh():
    while True:
        time.sleep(60)


if __name__ == "__main__":
    print("Bot Started!", file=sys.stderr)
    thread = Thread(target=chatgpt_refresh)
    thread.start()
    app.start(8080)  # POST http://localhost:4000/slack/events
