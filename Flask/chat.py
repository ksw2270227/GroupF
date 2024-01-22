from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, g
import sqlite3
import datetime

chat_bp = Blueprint('chat', __name__)


def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn


@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        message_content = request.form['message_content']

        if message_content.strip() != '':
            sender_user_id = 1  # ログインユーザーのIDを固定
            receiver_user_id = 2  # 受信者のユーザーIDを管理者に固定
            sender_role = session.get('role')  # 役割を'User'と仮定
            

            sent_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            save_message_to_database(sender_user_id, sender_role, receiver_user_id, 'Admin', message_content, sent_time)

            return redirect(url_for('chat.chat'))

    chat_history = get_chat_history()
    return render_template('chat.html', chat_history=chat_history)

def save_message_to_database(sender_user_id, sender_role, receiver_user_id, receiver_role, message_content, sent_time):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO messages (sender_user_id, sender_role, receiver_user_id, receiver_role, message_content, sent_time) VALUES (?, ?, ?, ?, ?, ?)',
                   (sender_user_id, sender_role, receiver_user_id, receiver_role, message_content.strip(), sent_time))

    conn.commit()
    cursor.close()
    conn.close()

def get_chat_history():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ユーザーまたは管理者としての履歴を取得
    cursor.execute('SELECT * FROM messages WHERE (sender_user_id = ? AND sender_role = ?) OR (sender_user_id = ? AND sender_role = ?)',
                   (1, session.get('role'), 2, 'Admin'))

    chat_history = cursor.fetchall()

    cursor.close()
    conn.close()

    return chat_history
