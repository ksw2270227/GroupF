from flask import Blueprint, render_template, session

index_bp = Blueprint('index', __name__)

signup_bp = Blueprint('signup', __name__)
login_bp = Blueprint('login', __name__)

mypage_bp = Blueprint('mypage', __name__)
chat_bp = Blueprint('chat', __name__)
group_bp = Blueprint('group', __name__)
map_bp = Blueprint('map', __name__)
logout_bp = Blueprint('logout', __name__)

# ルート設定
@index_bp.route('/index')
def index():
    user_id = session.get('user_id')
    return render_template('header.html', user_id=user_id)

# 未ログイン
@signup_bp.route('/signup')
def signup():
    user_id = session.get('user_id')
    return render_template('header.html', user_id=user_id)

@login_bp.route('/login')
def login():
    user_id = session.get('user_id')
    return render_template('header.html', user_id=user_id)


# ログイン済み
@mypage_bp.route('/mypage')
def chat():
    user_id = session.get('user_id')
    return render_template('header.html', user_id=user_id)

@chat_bp.route('/chat')
def chat():
    user_id = session.get('user_id')
    return render_template('header.html', user_id=user_id)

@map_bp.route('/map')
def map():
    user_id = session.get('user_id')
    return render_template('header.html', user_id=user_id)

@logout_bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    return render_template('header.html', user_id=user_id)