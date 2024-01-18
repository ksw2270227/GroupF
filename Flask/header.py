from flask import Blueprint, render_template, session

header_bp = Blueprint('header', __name__)

# @header_bp.route('/header')
# def render_header():
#     # セッションからユーザーIDを取得
#     user_id = session.get('user_id')

#     # ログイン状態によって表示するメニューを変更
#     if user_id:
#         menu_items = [
#             {'url': 'mypage.html', 'label': 'マイページ'},
#             {'url': 'chat.html', 'label': 'チャット'},
#             {'url': 'map.html', 'label': 'マップ'},
#             {'url': 'group.html', 'label': 'グループ'},
#             {'url': 'logout', 'label': 'ログアウト'}
#         ]
#     else:
#         menu_items = [
#             {'url': 'signup.html', 'label': '新規登録'},
#             {'url': 'login.html', 'label': 'ログイン'}
#         ]

#     return render_template('header.html', menu_items=menu_items)

# ルート設定
@header_bp.route('/index')
def index():
    return render_template('index.html')

@header_bp.route('/signup')
def signup():
    return render_template('signup.html')

@header_bp.route('/login')
def login():
    return render_template('login.html')

@header_bp.route('/chat')
def chat():
    return render_template('chat.html')