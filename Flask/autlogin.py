# login.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3

login_bp = Blueprint('login', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@login_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    error = None
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザーを検索
        cursor.execute(
            'SELECT * FROM users WHERE email_address = ? AND password = ?', (email_address, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # ユーザーIDをセッションに格納
            session['user_id'] = user[0]
            # ログイン成功時のリダイレクト先（例：indexページ）
            return redirect(url_for('index.index'))
        else:
            # ログイン失敗時のエラーメッセージ
            error = '無効なメールアドレスまたはパスワードです。'

    # GETリクエストの場合、またはエラーがある場合にログインページを表示.
    return render_template('login.html', error=error)

@login_bp.route('/autoLogin')
def auto_login():
    email_address = 'yamamoto@example.com'
    password = 'yama2024'

    conn = get_db_connection()
    cursor = conn.cursor()

    # ユーザーを検索
    cursor.execute(
        'SELECT * FROM users WHERE email_address = ? AND password = ?', (email_address, password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        # ユーザーIDをセッションに格納
        session['user_id'] = user[0]
        # 自動ログイン成功時のリダイレクト先（例：indexページ）
        return redirect(url_for('index.index'))
    else:
        # 自動ログイン失敗時のエラーメッセージ（任意の処理を追加する）
        flash('自動ログインに失敗しました。')

    # 自動ログインが成功しなかった場合のリダイレクト先（例：ログインページ）
    return redirect(url_for('login.login_user'))
