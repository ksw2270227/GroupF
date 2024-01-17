from flask import Flask, render_template, request
import mysql.connector
from flask import Blueprint

chat_bp = Blueprint('chat', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

def create_messages_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # messagesテーブルが存在しない場合に作成するクエリ
    create_table_query = """
    CREATE TABLE IF NOT EXISTS messages (
        message_id INT AUTO_INCREMENT PRIMARY KEY,
        sender_user_id VARCHAR(10),
        receiver_user_id VARCHAR(10),
        message_content TEXT,
        sent_time DATETIME
    )
    """

    cursor.execute(create_table_query)
    conn.commit()

    cursor.close()
    conn.close()


@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    create_messages_table()  # アプリケーション起動時にテーブルを作成
    if request.method == 'POST':
        message_content = request.form['message']
        save_message(message_content)

    messages = get_messages()

    return render_template('chat.html', messages=messages)

def save_message(message_content):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (message_content) VALUES (%s)', (message_content,))
    conn.commit()
    cursor.close()
    conn.close()

def get_messages():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM messages ORDER BY sent_time DESC')
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages

