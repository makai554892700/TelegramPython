from ..models import db, TAGInfo
from . import telegram
import jsonpickle


# 列出所有tag信息
@telegram.route('/listAllTAG')
def list_all_tag():
    tags = db.session.query(TAGInfo).all()
    return jsonpickle.encode(tags)


# 添加tag
@telegram.route('/addTAG/<tag_name>/<tag_desc>')
def add_tag(tag_name, tag_desc):
    tag_info = TAGInfo(tag_name=tag_name, tag_desc=tag_desc)
    try:
        db.session.add(tag_info)
        db.session.commit()
        db.session.close()
    except:
        return "save tag info have error."
    return "add tag."
