from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask import Blueprint

group_bp = Blueprint('group', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@group_bp.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        # データベースへの接続とユーザーの追加
        conn = get_db_connection()
        cursor = conn.cursor()

        # 以下は適切なテーブルとカラム名に変更する必要があります
        cursor.execute('INSERT INTO users (username, email) VALUES (%s, %s)', (username, email))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('group.show_users'))  # 成功時に表示するページにリダイレクト

@group_bp.route('/group')
def show_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('group.html', users=users)
