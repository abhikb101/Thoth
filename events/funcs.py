import re
from gpt import chatbot
import sys 

from firebase_db import db
from slack import slack_client
from firebase_db import db
from firebase_admin import firestore
from revChatGPT.V3 import Chatbot
from dotenv import load_dotenv
from utils.constants import user_pattern
import sys
from gpt import chatbot

import re
import sys

def get_user_by_id(user_id):
    user = db.collection('Users').document(user_id).get().to_dict()
    return user['profile']['real_name']

def set_reflections(data):
    db.collection('Reflections').document(data["id"]).set(data)

def create_reflection_model_data(message_array):
    # users = db.collection('Users').get()
    # messages = db.collection("MemoryStream").get()
    # user_ids = {}
    # for user in users:
    #     user_ids[user.to_dict().get("id")] = user.to_dict().get("profile").get("real_name")
    
    t_d = ""
    for message in message_array:
        t_d += message['text'] + "\n"

    return t_d

def create_prompt(data):
    initial = "I want you to be my coach and my goal is to read the long conversational slack threads This will be like a morning dialogue for me. I want you to go through a chat this thread, analyze it for me and give me a 3 bullet point summary of the conversation in not more than 70 words. Additionally highlight the wins and misses. Suggest actionables if any. Here is the transcript"
    return initial + "\n" + data

def upload_to_db(data):
    users = data[0]['users']
    uuid = data[0]['id']
    for user in users:
        doc_ref = db.collection('MemoryStream').document(user).set({uuid: data})


def get_all_messages(thread_ts, channel):
    print(thread_ts, channel)
    resp = slack_client.conversations_replies(ts=thread_ts, channel=channel)
    message_array = []
    # users_mapping = {}
    log = ""
    uuid = ""
    for message in resp['messages']:
        for k in message:
            if k == "text":
                print(k, message['text'])
                message_array.append({ "text": message['text']})

        # if message.get('user', False) and message['user'] not in users_mapping:
        #     print(message['user'])
        #     user_name = get_user_by_id(message['user'])
        #     users_mapping[message['user']] = user_name
        
        # users_in_message = re.findall(user_pattern, message_text)

        # for user in users_in_message:
        #     if user not in users_mapping:
        #         user_name = get_user_by_id(user[2:-1])
        #         users_mapping[user[2:-1]] = user_name  

        # uuid = channel + "-" + thread_ts
        # message_obj = {
        #     "id": channel + "-" + thread_ts,
        #     # "user": message.get('user', None),
        #     # "name": users_mapping[message.get('user', None)],
        #     "text": message_text,
        #     # "files": message.get('files', None),
        #     # "ts": message.get('ts', None)
        # }

        # message_array.append(message_obj)

    # for i in range(0, len(message_array)):
    #     for key in users_mapping:
    #         if '<@'+ key + '>' in message_array[i]['text']:
    #             message_array[i]['text'] = message_array[i]['text'].replace('<@'+ key + '>', users_mapping[key])


    # for i in range(0, len(message_array)):
    #     message_array[i]['users'] = users_mapping

    # upload_to_db(message_array)

    return message_array


def summarize_data(thread_ts, channel):
    message_array = get_all_messages(thread_ts, channel)
    print(message_array)
    data = create_reflection_model_data(message_array)

    prompt = create_prompt(data)
    convo_id = ""

    response = chatbot.ask(prompt, convo_id=convo_id)
    # ref = {"id": uuid, "text": data[uuid]['text'], "reflections": response, "users": data[uuid].get('users', None)}
    return response

def handle_event(event, is_mention):
    prompt = re.sub("\\s<@[^, ]*|^<@[^, ]*", "", event["text"])
    convo_id = event.get("thread_ts") or event.get("ts") or ""
    try:
        response = chatbot.ask(prompt, convo_id=convo_id)
        user = event["user"]
        if is_mention:
            response = f"<@{user}> {response}"
    except Exception as e:
        print(e, file=sys.stderr)
        response = "We are experiencing exceptionally high demand. Please, try again."

    if is_mention:
        original_message_ts = event["ts"]
    else:
        original_message_ts = None

    # Use the `app.event` method to send a message
    return {"response": response, "thread_ts": original_message_ts}