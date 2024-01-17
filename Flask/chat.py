from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask import Blueprint

chat_bp = Blueprint('chat', __name__)

# SQLiteデータベースへの接続を取得する関数
def get_db_connection():
    conn = sqlite3.connect('your_database.db')  # ここでデータベース名を適切に指定してください
    return conn

@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        # メッセージの保存処理
        message_content = request.form['messageInput']
        sender_user_id = 'ユーザー1'  # ダミーデータとしてユーザー1としていますが、実際にはユーザーIDを取得する必要があります
        receiver_user_id = 'ユーザー2'  # ダミーデータとしてユーザー2としていますが、実際にはユーザーIDを取得する必要があります

        if message_content:
            conn = get_db_connection()
            cursor = conn.cursor()

            # messagesテーブルにデータを挿入
            cursor.execute("INSERT INTO messages (sender_user_id, receiver_user_id, message_content) VALUES (?, ?, ?)",
                           (sender_user_id, receiver_user_id, message_content))

            conn.commit()
            conn.close()

    # メッセージの表示処理
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages')
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('chat.html', messages=messages)
