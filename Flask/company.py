from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

company_bp = Blueprint('company', __name__)

# データベースとの接続を確立する関数
def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@company_bp.route('/company', methods=['GET', 'POST'])
def save_company_info():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        group_id = request.form['group_id']
        group_name = request.form['group_name']
        password = request.form['password']
        user_id = request.form['user_id']
        creation_date = request.form['creation_date']
        max_members = request.form['max_members']
        current_members = request.form['current_members']
        event_id = request.form['event_id']

        try:
            # ユーザー情報をusersテーブルに挿入
            cursor.execute('INSERT INTO users (group_id, group_name, password, user_id, creation_date, max_members, current_members, event_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                            (group_id, group_name, password, user_id, creation_date, max_members, current_members, event_id))
            conn.commit()
            message = "企業情報が正常に保存されました。"
        except Exception as e:
            conn.rollback()
            message = f"エラーが発生しました: {str(e)}"
        finally:
            cursor.close()
            conn.close()

        return render_template('company_saved.html', message=message)
    elif request.method == 'GET':
        # GETリクエストの場合、単にフォームページを表示するだけ
        return render_template('company.html')
