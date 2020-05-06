from ..models import db, Message
from . import telegram
from flask import request
import jsonpickle
# from .telegram_client import user_1, user_2, user_3, user_4
from .telegram_client import user_1


# 列出所有tag信息
@telegram.route('/listAllMessage')
def list_all_message():
    messages = db.session.query(Message).all()
    return jsonpickle.encode(messages)


# 添加tag
@telegram.route('/addMessage/<message_desc>', methods=["POST"])
def add_message(message_desc):
    message = bytes.decode(request.get_data())
    message_info = Message(message=message, message_desc=message_desc)
    try:
        db.session.add(message_info)
        db.session.commit()
        db.session.close()
    except:
        return "save message info have error."
    return "add tag."


# 发送消息
@telegram.route('/sendMessageByUser', methods=['POST'])
def send_message_by_user():
    json_data = request.get_json()
    if json_data is not None and dict.__contains__(json_data, "user") \
            and dict.__contains__(json_data, "user") \
            and dict.__contains__(json_data, "username"):
        user = json_data["user"]
        message = json_data["message"]
        username = json_data["username"]
        if user == 1:
            user_1.send_message(username, message)
        # elif user == 2:
        #     user_2.send_message(username, message)
        # elif user == 3:
        #     user_3.send_message(username, message)
        # elif user == 4:
        #     user_4.send_message(username, message)
        else:
            return "no_user type error"
    else:
        return "no_data error."
    return "ok"
