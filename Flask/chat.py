from flask import Flask, render_template, request
import mysql.connector
import sqlite3
from flask import Blueprint

chat_bp = Blueprint('chat', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn


@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
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

