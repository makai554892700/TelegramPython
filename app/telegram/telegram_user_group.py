# from .telegram_client import user_1, user_2, user_3, user_4
from .telegram_client import user_1
from sqlalchemy.exc import IntegrityError
from ..models import db, UserGroup, UserTAGInfo
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, Channel, InputUser, InputChannel
import base64, threading, jsonpickle
from . import telegram
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest

saving_group = ""
is_updating_all_user_group = False
is_updating_group_tag = False
id_add_users_2_channel = False


# 保存所有群组信息
def save_all_group_fun():
    try:
        print('save all group fun.')
        global is_updating_all_user_group
        responses = user_1.iter_dialogs(1000)
        if responses is not None:
            try:
                for response in responses:
                    if isinstance(response.entity, Channel):
                        save_group(response.entity.id, response.entity.title, response.entity.access_hash,
                                   response.entity.username, 0, False)
                db.session.close()
            except:
                print("foreach respons have error.")
        else:
            print("response is none.")
        is_updating_all_user_group = False
        print('update user group finish.')
    except:
        is_updating_all_user_group = False
        print('update user group finish.but get error.')


# 保存指定群组信息
def save_group(in_id, in_title, in_access_hash, in_user_name, in_tag_id, need_close: bool):
    print('save group.')
    try:
        group = db.session.query(UserGroup).filter(UserGroup.group_id == in_id).scalar()
    except IntegrityError:
        print("have errr.save group finish.")
        return
    if in_title is None:
        title = None
    else:
        title = bytes.decode(base64.b64encode(in_title.encode('utf-8')))
    if title is not None and len(title) > 254:
        title = "str too long."
    if group is None:
        group = UserGroup(group_id=in_id, access_hash=in_access_hash,
                          title=title, username=in_user_name, tag_id=in_tag_id)
        db.session.add(group)
        print('insert usergrouping.......')
    else:
        group.group_id = in_id
        group.access_hash = in_access_hash
        group.title = title
        group.username = in_user_name
    try:
        db.session.commit()
    except IntegrityError:
        print('save group have a error.')
    if need_close:
        db.session.close()
    print("save group finish.")


# 更新群组tag
def update_group_fun(in_group_id: int, in_tag_id: int):
    try:
        global is_updating_group_tag
        user_group = db.session.query(UserGroup).filter(UserGroup.group_id == in_group_id).scalar()
        if user_group is None:
            return
        else:
            user_group.tag_id = in_tag_id
            user_tag_infos = db.session.query(UserTAGInfo).filter(UserGroup.group_id == in_group_id).all()
            for user_tag_info in user_tag_infos:
                user_tag_info.tag_id = in_tag_id
                try:
                    db.session.add(user_tag_info)
                    db.session.commit()
                except IntegrityError:
                    print("update user tag info error.")
                    continue
            try:
                db.session.add(user_group)
                db.session.commit()
                db.session.close()
            except IntegrityError:
                return
        is_updating_group_tag = False
        print("update group finished.")
    except:
        is_updating_group_tag = False
        print("update group finished.but get error.")


def add_users_2_channel_fun(user_group_id: int, tag_id: int):
    print('start add users 2 channel.')
    try:
        global id_add_users_2_channel
        user_group = db.session.query(UserGroup).filter(UserGroup.group_id == user_group_id).scalar()
        if user_group is None:
            print('user group is none.')
        else:
            inputChannel = InputChannel(channel_id=user_group.group_id
                                        , access_hash=user_group.access_hash)
            user_tag_infos = db.session.query(UserTAGInfo).filter(
                UserGroup.tag_id == tag_id).all()
            if user_tag_infos is None:
                print("user tag infos is none.")
            else:
                inputUsers = []
                all_count = len(user_tag_infos)
                count = 1
                for user_tag_info in user_tag_infos:
                    inputUser = InputUser(user_id=int(user_tag_info.user_id)
                                          , access_hash=int(user_tag_info.user_hash))
                    try:
                        user_1(InviteToChannelRequest(inputChannel, [inputUser]))
                    except:
                        print("invite to channel error.userId="
                              + str(user_tag_info.user_id)
                              + ";userHash=" + str(user_tag_info.user_hash))
                #     inputUsers.append(inputUser)
                #     if count % 100 == 0 or all_count == count:
                #         print('add users 2 channel.')
                #         try:
                #             client(InviteToChannelRequest(inputChannel, inputUsers))
                #         except:
                #             print("invite to channel error." + str(user_tag_info.user_id))
                #         inputUsers.clear()
                #     count += 1
                # print('all_count=' + str(all_count) + ';count=' + str(count))
        id_add_users_2_channel = False
        print('add users 2 channel finish.')
    except:
        id_add_users_2_channel = False
        print('add users 2 channel get error.')


# 添加用户到群组
@telegram.route('/addUsers2Channel/<user_group_id>/<tag_id>')
def add_users_2_channel(user_group_id: int, tag_id: int):
    global id_add_users_2_channel
    if id_add_users_2_channel:
        return 'is adding user 2 channel.'
    else:
        id_add_users_2_channel = True
        th = threading.Thread(target=add_users_2_channel_fun, args=(user_group_id, tag_id))
        th.start()
        return 'adding user 2 channel.'


# 首页 装饰器 装饰器函数
@telegram.route('/getSavingGroup')
def get_saving_group():
    # user = client.get_entity("@Jude12")
    # print(user)
    # channel = client.get_entity("@mktesttttttttttt")
    # print(channel)
    # channel_id = channel.id
    # channel_hash = channel.access_hash
    # user_id = user.id
    # user_hash = user.access_hash
    channel_id = 1247985828
    channel_hash = -8866180916535177199
    user_id = 490342664
    user_hash = -7707849152056625292
    inputChannel = InputChannel(channel_id=channel_id, access_hash=channel_hash)
    print(inputChannel)
    inputUser = InputUser(user_id=user_id, access_hash=user_hash)
    print(inputUser)
    test = user_1(InviteToChannelRequest(inputChannel, [inputUser]))
    print(test)
    return "saving group is:" + saving_group


# 列出群组所有用户 @username url chat#id user#id channel#id #->%23
@telegram.route('/getInfo/<infoType>/<info>')
def get_info(infoType, info):
    print("infoType=" + infoType + ";info=" + info)
    result = None
    if "user" == infoType:
        result = user_1.get_entity(PeerUser(info))
    elif "chat" == infoType:
        result = user_1.get_entity(PeerChat(info))
    elif "channel" == infoType:
        result = user_1.get_entity(PeerChannel(int(info)))
    elif "id" == infoType:
        result = user_1.get_entity(info)
    print(result)
    # return jsonpickle.encode(result, False)
    return "get group info."


# 列出所有群组
@telegram.route('/listAllGroup/<user_id>')
def list_all_group(user_id: int):
    try:
        if user_id == "1":
            responses = user_1.iter_dialogs(10000)
        # elif user_id == "2":
        #     responses = user_2.iter_dialogs(10000)
        # elif user_id == "3":
        #     responses = user_3.iter_dialogs(10000)
        # elif user_id == "4":
        #     responses = user_4.iter_dialogs(10000)
        else:
            return "user_id must be 1/2/3/4;now user id = " + str(user_id)
    except:
        return "get responses error."
    if responses is not None:
        for response in responses:
            print(response)
            # if isinstance(response.entity, Channel):
            #     print(response)
            #     print("---------------\n")
        print("list all group done.\n")
    else:
        print("response is none.")
    return "list all group."


# 保存所有群组
@telegram.route('/saveAllGroup')
def save_all_group():
    global is_updating_all_user_group
    if is_updating_all_user_group:
        return 'is updating user group.'
    else:
        is_updating_all_user_group = True
        th = threading.Thread(target=save_all_group_fun)
        th.start()
        return "save all group."


# 列出数据库所有群组
@telegram.route('/listAllDBGroup')
def list_all_db_group():
    user_groups = db.session.query(UserGroup).all()
    return jsonpickle.encode(user_groups)


# 更新数据库tag
@telegram.route('/updateGroupTAG/<group_id>/<tag_id>')
def update_group_tag(group_id: int, tag_id: int):
    global is_updating_group_tag
    if is_updating_group_tag:
        return 'is updating group tag.'
    else:
        is_updating_group_tag = True
        th = threading.Thread(target=update_group_fun, args=(int(group_id), int(tag_id)))
        th.start()
        return "update group tag."
