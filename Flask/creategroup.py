from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask import Blueprint

creategroup_bp = Blueprint('creategroup', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@creategroup_bp.route('/creategroup', methods=['GET', 'POST'])
def create_group():

    if 'user_id' not in session:
        return redirect(url_for('login.login_user'))

    if request.method == 'POST':
        print("formからデータを取得します")
        # フォームからデータを受け取り
        group_name = request.form['group_name']
        password = request.form['password']
        max_members = request.form['man']  # フォームの input 要素の名前が 'man' なのでこちらを指定

        # データベースに挿入する処理
        conn = get_db_connection()
        cursor = conn.cursor()
        user_id = session.get('user_id')  # セッションからユーザーIDを取得

        # 追加: 一意の制約を追加する
        try:
            cursor.execute(
                'INSERT INTO groups (group_name, password, user_id, creation_date, max_members, current_members, event_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (group_name, password, user_id, '2023-01-17 12:00:00', max_members, 0, 0)
            )
        except sqlite3.IntegrityError as e:
            # 重複がある場合の処理
            print("追加: 重複があります。")
            conn.rollback()
        else:
            # 重複がない場合の処理
            print("追加: 成功")
            conn.commit()
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('group.group_page'))  # 仮に/indexにリダイレクト
    
    return render_template('creategroup.html')  # グループ作成フォームを表示