# group.py

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask import Blueprint

group_bp = Blueprint('group', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@group_bp.route('/group', methods=['GET', 'POST'])
def create_group():
    conn = None
    cursor = None
    

    try:
        groups = []  # 初期化
        participants = []  # 参加者情報の初期化
        group_count = 0  # group_count を初期化
        max_participants = 0  # max_participants を初期化

        if request.method == 'POST':
            # フォームの送信を処理するコード

        # ログインユーザーのメールアドレスからユーザーIDを取得
            user_email = session.get('user_email')  # セッションからユーザーのメールアドレスを取得（例）

        # ユーザーIDを使って関連するグループ情報を取得
        if user_email:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # ユーザーIDの取得（例：usersテーブルにid列がある場合）
            cursor.execute('SELECT id FROM users WHERE email = %s', (user_email,))
            user_id = cursor.fetchone()['id']

            # ユーザーIDを使って関連するグループ情報を取得
            cursor.execute('SELECT group_name, group_id, max_participants FROM groups WHERE user_id = %s', (user_id,))
            groups = cursor.fetchall()


        # GETメソッドの場合はデータベースから情報を取得してテンプレートに渡す
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # グループ情報を取得
            cursor.execute('SELECT group_name, group_id FROM groups')
            groups = cursor.fetchall()

            # 参加者情報を取得
            cursor.execute('SELECT participant_name FROM participants')
            participants = cursor.fetchall()

            # グループの人数を取得
            cursor.execute('SELECT COUNT(*) as group_count FROM groups')
            group_count = cursor.fetchone()['group_count']

            # 最大参加者数を取得
            cursor.execute('SELECT MAX(max_participants) as max_participants FROM groups')
            max_participants = cursor.fetchone()['max_participants']


    except Exception as e:
        print(f"エラー: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('group.html', groups=groups, participants=participants, group_count=group_count, max_participants=max_participants)