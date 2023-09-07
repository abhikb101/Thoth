from dotenv import dotenv_values
import os

config = dotenv_values("vendorlabs.env")

SLACK_CLIENT_ID=config.get("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET=config.get("SLACK_CLIENT_SECRET")
SLACK_SIGNING_SECRET=config.get("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN=config.get("SLACK_BOT_TOKEN")
OPENAI_API_KEY=config.get("OPENAI_API_KEY")
JIRA_EMAIL=config.get("JIRA_EMAIL")
JIRA_API_KEY=config.get("JIRA_API_KEY")
FIREBASE_PATH=config.get("FIREBASE_PATH")
FIREBASE_APPLICATOIN=config.get("FIREBASE_APPLICATOIN")
OPENAI_ENGINE=config.get("OPENAI_ENGINE")