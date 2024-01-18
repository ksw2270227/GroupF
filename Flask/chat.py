from flask import Flask, render_template, request, redirect, url_for, Blueprint
import sqlite3
import datetime

chat_bp = Blueprint('chat', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        # チャット画面からメッセージを取得
        message_content = request.form['message_content']

        if message_content.strip() != '':
            # 送信ユーザーIDと受信ユーザーIDは適切な値に設定する必要があります
            sender_user_id = '1'
            receiver_user_id = '2'

            # 現在の日時を取得
            sent_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # メッセージをデータベースに保存
            save_message_to_database(sender_user_id, receiver_user_id, message_content, sent_time)

            # メッセージを保存したらリダイレクト
            return redirect(url_for('chat.chat'))

    # チャット履歴を取得して表示
    chat_history = get_chat_history()
    return render_template('chat.html', chat_history=chat_history)


def save_message_to_database(sender_user_id, receiver_user_id, message_content, sent_time):
    conn = get_db_connection()
    cursor = conn.cursor()

    # メッセージをmessagesテーブルに挿入
    cursor.execute('INSERT INTO messages (sender_user_id, receiver_user_id, message_content, sent_time) VALUES (?, ?, ?, ?)',
                   (sender_user_id, receiver_user_id, message_content.strip(), sent_time))

    conn.commit()
    cursor.close()
    conn.close()

def get_chat_history():
    conn = get_db_connection()
    cursor = conn.cursor()

    # messagesテーブルからチャット履歴を取得
    cursor.execute('SELECT * FROM messages')
    chat_history = cursor.fetchall()

    cursor.close()
    conn.close()

    return chat_history
