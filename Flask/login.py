from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask import Blueprint

login_bp = Blueprint('login', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # パスワードのハッシュ化はセキュリティ上の理由で必要ですが、
        # この例では簡略化のため省略しています。実際には適切なハッシュ関数を使用してください。

        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザーが存在するか確認
        cursor.execute('SELECT * FROM users WHERE user_name = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # 既に同じユーザー名が存在する場合の処理をここに追加するか、
            # ユーザーに通知してください。

            return render_template('login.html', message='ユーザー名は既に存在します。')

        # ユーザーが存在しない場合は新しいユーザーを挿入
        cursor.execute('INSERT INTO users (user_name, password) VALUES (%s, %s)', (username, password))
        conn.commit()

        cursor.close()
        conn.close()

        # 登録が成功した場合、適切なリダイレクト先に変更してください。
        return redirect(url_for('index.index'))

    return render_template('login.html', message='')

# この部分でアプリケーションにBlueprintを登録します。
# app.register_blueprint(login_bp)  # app.pyで行うことが一般的
