from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # ログイン情報をデータベースに保存する処理
        save_login_info(email, password)

        return redirect(url_for('success'))

    return render_template('login.html')

def save_login_info(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 注意: 以下は簡易的な例で、実際のアプリケーションではパスワードのハッシュ化などのセキュリティ対策が必要です。
    cursor.execute('INSERT INTO users (email_address, password) VALUES (%s, %s)', (email, password))

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/success')
def success():
    return 'ログイン情報が正常に保存されました。'

if __name__ == '__main__':
    app.run(debug=True)
