from . import main
from ..models import db, User


@main.route('/', methods=['GET', 'POST'])
def index():
    user = User(user_id=3, access_hash=3)
    try:
        db.session.add(user)
        db.session.commit()
        db.seesion.close()
    except:
        print('have error.')
        print(sys.exc_info()[0])
    return 'hello world main.'
