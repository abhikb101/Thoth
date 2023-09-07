import logging
import os
import sys
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from settings import SLACK_BOT_TOKEN

slack_client = WebClient(token=SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)