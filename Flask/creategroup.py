from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask import Blueprint

creategroup_bp = Blueprint('creategroup', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@creategroup_bp.route('/creategroup', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        # フォームからデータを受け取り
        group_name = request.form['group_name']
        password = request.form['password']
        max_members = request.form['man']  # フォームの input 要素の名前が 'man' なのでこちらを指定

        # データベースに挿入する処理
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO groups (password, user_id, creation_date, max_members, current_members, event_id) VALUES (?, ?, ?, ?, ?, ?)',
            (password, 1, '2023-01-17 12:00:00', max_members, 0, 0)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('group.group'))  # グループ作成後に表示するページにリダイレクト
    
    return render_template('creategroup.html')  # グループ作成フォームを表示
