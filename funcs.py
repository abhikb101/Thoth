from firebase_db import db
from slack import slack_client
from firebase_db import db
from firebase_admin import firestore
from revChatGPT.V3 import Chatbot
from dotenv import load_dotenv

import sys
load_dotenv()
ChatGPTConfig = {
    "api_key": "",
}
chatbot = Chatbot(**ChatGPTConfig)
import re
import sys

def get_user_by_id(user_id):
    user = db.collection('Users').document(user_id).get().to_dict()
    return user['profile']['real_name']

def set_reflections(data):
    db.collection('Reflections').document(data["id"]).set(data)

def create_reflection_model_data():
    users = db.collection('Users').get()
    messages = db.collection("MemoryStream").get()
    user_ids = {}
    for user in users:
        user_ids[user.to_dict().get("id")] = user.to_dict().get("profile").get("real_name")
    
    traning_data = {}
    for message in messages:
        t_d = ""
        m_id = None
        message_dict = message.to_dict()
        users = {}
        for k in message_dict:
            m_id = k
            decodec_message = message_dict[k]
            users = decodec_message[0]['users']
            for d_m in decodec_message: 
                t_d += d_m["name"] + ": "+ d_m['text'] + "\n"
        traning_data[k] = {"text": t_d, "users": users}

    return traning_data

def create_prompt(data):
    initial = "I want you to be my coach and my goal is to read the long conversational slack threads This will be like a morning dialogue for me. I want you to go through a chat this thread, analyze it for me and give me a 3 bullet point summary of the conversation in not more than 70 words. Additionally highlight the wins and misses. Suggest actionables if any. Here is the transcript"

    return initial + "\n" + data

def upload_to_db(data):
    users = data[0]['users']
    uuid = data[0]['id']
    for user in users:
        doc_ref = db.collection('MemoryStream').document(user).set({uuid: data})


def get_all_messages(thread_ts, channel):
    resp = slack_client.conversations_replies(ts=thread_ts, channel=channel)
    message_array = []
    users_mapping = {}
    log = ""
    pattern = r"<@[A-Z\d]+>"
    uuid = ""
    for message in resp['messages']:
        message_text  = message.get('text', None)


        if message.get('user', False) and message['user'] not in users_mapping:
            print(message['user'])
            user_name = get_user_by_id(message['user'])
            users_mapping[message['user']] = user_name
        
        users_in_message = re.findall(pattern, message_text)

        for user in users_in_message:
            if user not in users_mapping:
                user_name = get_user_by_id(user[2:-1])
                users_mapping[user[2:-1]] = user_name  

        uuid = channel + "-" + thread_ts
        message_obj = {
            "id": channel + "-" + thread_ts,
            "user": message.get('user', None),
            "name": users_mapping[message.get('user', None)],
            "text": message_text,
            # "files": message.get('files', None),
            # "ts": message.get('ts', None)
        }

        message_array.append(message_obj)

    for i in range(0, len(message_array)):
        for key in users_mapping:
            if '<@'+ key + '>' in message_array[i]['text']:
                message_array[i]['text'] = message_array[i]['text'].replace('<@'+ key + '>', users_mapping[key])


    for i in range(0, len(message_array)):
        message_array[i]['users'] = users_mapping

    upload_to_db(message_array)

    return uuid


def summarize_data(thread_ts, channel):
    uuid = get_all_messages(thread_ts, channel)

    data = create_reflection_model_data()

    prompt = create_prompt(data[uuid]['text'])
    convo_id = ""

    response = chatbot.ask(prompt, convo_id=convo_id)
    ref = {"id": uuid, "text": data[uuid]['text'], "reflections": response, "users": data[uuid].get('users', None)}
    return response
