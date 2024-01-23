from flask import Flask, render_template, request, redirect, url_for, Blueprint, session
import sqlite3
import datetime

selectchatpartner_bp = Blueprint('selectchatpartner', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@selectchatpartner_bp.route('/selectchatpartner', methods=['GET'])
def selectchatpartner():
    users = get_users_with_latest_chat()
    return render_template('selectchatpartner.html', users=users)

def get_users_with_latest_chat():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT users.user_id, users.user_name, MAX(messages.sent_time) as latest_chat_time, messages.message_content as latest_chat_content FROM users LEFT JOIN messages ON (users.user_id = messages.sender_user_id AND users.user_id = messages.receiver_user_id) GROUP BY users.user_id')

        users = []
        for row in cursor.fetchall():
            user = {
                'user_id': row[0],
                'user_name': row[1],
                'latest_chat_time': row[2] if row[2] is not None else 'N/A',
                'latest_chat_content': row[3] if row[3] is not None else 'No chat history'
            }
            users.append(user)

        cursor.close()
        conn.close()

        return users
    except Exception as e:
        print(f"Error fetching users with latest chat: {e}")
        return None

# ... (existing functions from chat.py)
