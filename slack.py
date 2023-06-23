import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_client = WebClient(token="xoxb-274866499440-5415960708913-jt5lgnY7XtUAdYdUkFuokjNW")
logger = logging.getLogger(__name__)