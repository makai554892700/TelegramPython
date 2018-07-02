from . import db
from sqlalchemy.schema import UniqueConstraint, Index


# 已保存的群组对象
class SavedGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer)
    Index(group_id)
    UniqueConstraint(group_id)


# 用户对象
class User(db.Model):
    user_id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    access_hash = db.Column(db.BigInteger)
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    Index(username)
    UniqueConstraint(user_id)


# 用户群组对象
class UserGroup(db.Model):
    group_id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    access_hash = db.Column(db.BigInteger)
    title = db.Column(db.String(255))
    username = db.Column(db.String(255))
    tag_id = db.Column(db.Integer)
    Index(username)
    UniqueConstraint(group_id)


# 标签对象
class TAGInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(255), nullable=False)
    tag_desc = db.Column(db.Text)


# 用户tag描述对象
class UserTAGInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer)
    user_id = db.Column(db.BigInteger)
    user_name = db.Column(db.String(255))
    user_hash = db.Column(db.BigInteger)
    group_id = db.Column(db.BigInteger)
    group_name = db.Column(db.String(255))
    group_hash = db.Column(db.BigInteger)
    Index(tag_id, group_name)
    UniqueConstraint(user_id, group_id)


# 消息对象
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text)
    message_desc = db.Column(db.String(255))


# 用户发过的消息记录
class MessageHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger)
    message_id = db.Column(db.Integer)
    UniqueConstraint(user_id, message_id)
