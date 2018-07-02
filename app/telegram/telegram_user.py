from .telegram_client import user_1
from sqlalchemy.exc import IntegrityError
from ..models import db, User, SavedGroup, UserGroup, UserTAGInfo, Message, MessageHistory
from telethon.tl.types import PeerChannel
import base64, threading, time
from . import telegram

is_sending = False
is_updating_user = False
is_updating_all_user = False


# 更新保存用户信息
def update_user_fun(in_id, need_close: bool):
    try:
        global is_updating_user
        try:
            channel = user_1.get_entity(PeerChannel(int(in_id)))
            user_group = db.session.query(UserGroup).filter(UserGroup.group_id == in_id).scalar()
        except:
            print("get channel error.id=" + str(in_id))
            is_updating_user = False
            return
        if channel is None or user_group is None:
            print("channel is none or user group is None.")
            is_updating_user = False
            return
        try:
            responses = user_1.iter_participants(channel, aggressive=True)
        except:
            print("get channel error.id=" + in_id)
            is_updating_user = False
            return
        if responses is None:
            print("responses is none.")
            is_updating_user = False
            return
        responses_size = 0
        try:
            for response in responses:
                responses_size += 1
                # print(response)
                user = db.session.query(User).filter(User.user_id == response.id).scalar()
                if response.first_name is not None:
                    first_name = bytes.decode(base64.b64encode(response.first_name.encode('utf-8')))
                else:
                    first_name = None
                if response.last_name is not None:
                    last_name = bytes.decode(base64.b64encode(response.last_name.encode('utf-8')))
                else:
                    last_name = None
                if first_name is not None and len(first_name) > 254:
                    first_name = "str too long."
                if last_name is not None and len(last_name) > 254:
                    last_name = "str too long."
                if user is None:
                    user = User(user_id=response.id, access_hash=response.access_hash,
                                username=response.username,
                                first_name=first_name,
                                last_name=last_name,
                                phone=response.phone)
                    print('insert usering.......')
                else:
                    user.user_id = response.id
                    user.access_hash = response.access_hash
                    user.username = response.username
                    user.first_name = first_name
                    user.last_name = last_name
                    user.phone = response.phone
                try:
                    db.session.add(user)
                    db.session.commit()
                    user_tag_info = UserTAGInfo(
                        user_id=user.user_id, tag_id=user_group.tag_id
                        , group_id=user_group.group_id, group_name=user_group.username
                        , user_name=user.username, user_hash=user.access_hash
                        , group_hash=user_group.access_hash)
                    db.session.add(user_tag_info)
                    db.session.commit()
                except IntegrityError:
                    print('save user have an error.')
            saved_group = SavedGroup(group_id=int(in_id))
            db.session.add(saved_group)
            try:
                db.session.commit()
            except IntegrityError:
                print('save saved group have an error.')
            if need_close:
                db.session.close()
        except:
            print('get response error.')
        is_updating_user = False
        print("update user finish.responses_size=" + str(responses_size))
    except:
        is_updating_user = False
        print("update user finish.but get error.")


# 发送消息
def send_message_fun(message_type: str, id: int, message_id: int):
    i = 0
    error_message = None
    while i < 1:
        i = 1
        try:
            message_info = db.session.query(Message).filter(Message.id == message_id).scalar()
            if message_info is None:
                break
            message = message_info.message
            ids = []
            global is_sending
            tag_infos = None
            if message_type is None:
                error_message = "message type is none."
                break
            elif "user_id" == message_type:
                ids.append(id)
            elif "tag_id" == message_type:
                tag_infos = db.session.query(UserTAGInfo).filter(UserTAGInfo.tag_id == id).all()
            elif "group_id" == message_type:
                tag_infos = db.session.query(UserTAGInfo).filter(UserTAGInfo.group_id == id).all()
            else:
                error_message = "message type is error."
                break
            if tag_infos is not None:
                for tag_info in tag_infos:
                    if tag_info.user_name is not None:
                        ids.append(int(tag_info.user_id))
            if len(ids) == 0:
                error_message = "no user name to send."
                break
            else:
                for user_id in ids:
                    try:
                        message_history = db.session.query(MessageHistory).filter(
                            MessageHistory.user_id == user_id,
                            MessageHistory.message_id == message_id
                        ).scalar()
                        if message_history is None:
                            user_1.send_message(int(user_id), str(message))
                            time.sleep(10)
                            message_history = MessageHistory(user_id=user_id, message_id=message_id)
                            db.session.add(message_history)
                            db.session.commit()
                        else:
                            print("message is already send.user id=" + str(user_id)
                                  + ";message id=" + str(message_id))
                    except:
                        print("send message error.user id=" + str(user_id)
                              + ";message id=" + str(message_id) + ";message=" + str(message))
                        continue
                db.session.close()
        except:
            error_message = "have big error."
    print("send message finished.")
    if error_message is not None:
        print(error_message)
    is_sending = False


# 更新保存所有用户信息
def update_all_user_fun():
    try:
        global is_updating_all_user
        groups = db.session.query(UserGroup).all()
        if groups is not None:
            for group in groups:
                update_user_fun(int(group.group_id), False)
        else:
            print("groups is none.")
        db.session.close()
        is_updating_all_user = False
        print('update all user finish.')
    except:
        is_updating_all_user = False
        print('update all user finish.but get error.')


# 列出群组所有用户
@telegram.route('/listAllUser/<group>')
def list_all_user(group):
    channel = user_1.get_entity(group)
    print(channel)
    responses = user_1.iter_participants(channel, aggressive=True)
    count = 0
    if responses is not None:
        try:
            for response in responses:
                count += 1
                # print(response)
        except:
            print("response error.")
    else:
        return "response is none."
    return "list all user.count=" + str(count)


# 更新保存群组所有用户
@telegram.route('/updateAllUser')
def update_all_user():
    global is_updating_all_user
    if is_updating_all_user:
        return 'is updating user.'
    else:
        is_updating_all_user = True
        th = threading.Thread(target=update_all_user_fun)
        th.start()
        return "update all user."


# 更新保存群组所有用户
@telegram.route('/updateUserByGroupId/<id>')
def update_user(id):
    global is_updating_user
    if is_updating_user:
        return 'is updating user.'
    else:
        is_updating_user = True
        th = threading.Thread(target=update_user_fun, args=(int(id), True))
        th.start()
        return "update user by id."


# 发送信息给某用户
@telegram.route('/sendMessage/<message_type>/<key>/<message_id>')
def send_message(message_type: str, key: int, message_id: int):
    global is_sending
    if is_sending:
        return "is sending."
    is_sending = True
    try:
        th = threading.Thread(target=send_message_fun, args=(message_type, key, message_id))
        th.start()
    except:
        is_sending = False
        print("send message have error.thread error.")
    return "message_type=" + str(message_type) + ";key=" + str(key) + "."
