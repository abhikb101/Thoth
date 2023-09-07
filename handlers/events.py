from events.funcs import summarize_data, get_all_messages, handle_event
from integrations.jira_funcs import create_jira, is_jira_issue_intent


def handle_mention(event):        
    response = handle_event(event, is_mention=True)
    return response

def handle_summary(event, say):
    splitted = event['text'].split("/")
    channel_id = splitted[4]
    thread_ts = splitted[-1].split("?")[1].split("&")[0].split("=")[1]
    resp = summarize_data(thread_ts, channel_id)
    say(resp, thread_ts=event.get("thread_ts") or event.get("ts"))
    return

def handle_jira(event):
    try:
        create_jira(event['text'])
        return "It's done"
    except Exception as e:
        return "Something went wrong"

def handle_ask_thoth(event):
    return "yo"

def handle_message(event, say):
    print(event, say)