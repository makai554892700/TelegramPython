from flask import Blueprint

telegram = Blueprint('telegram', __name__)

from . import telegram_client, telegram_message, telegram_tag, telegram_user, telegram_user_group, errors
