from flask import Flask, render_template, request, redirect, url_for
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

@chat_bp.route('/chat')
def show_chat():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # メッセージテーブルから全てのメッセージを取得
        cursor.execute('SELECT * FROM messages ORDER BY sent_time')
        messages = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('chat.html', messages=messages)

    except Exception as e:
        return str(e)

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        try:
            # メッセージをデータベースに保存
            conn = get_db_connection()
            cursor = conn.cursor()

            sender_user_id = 'user1'  # 仮の値、実際のセッションや認証から取得するべき
            receiver_user_id = 'user2'  # 同上
            message_content = request.form['message']

            cursor.execute('INSERT INTO messages (sender_user_id, receiver_user_id, message_content) VALUES (%s, %s, %s)',
                           (sender_user_id, receiver_user_id, message_content))
            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('chat.show_chat'))

        except Exception as e:
            return str(e)

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(chat_bp)

    app.run(debug=True)
