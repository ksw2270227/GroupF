# group.py

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

@group_bp.route('/group', methods=['GET', 'POST'])
def create_group():
    conn = None
    cursor = None

    try:
        if request.method == 'POST':
            # フォームの送信を処理するコード

        # GETメソッドの場合はデータベースから情報を取得してテンプレートに渡す
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # グループ情報を取得
            cursor.execute('SELECT group_name, group_id FROM groups')
            groups = cursor.fetchall()

            # 参加者情報を取得
            cursor.execute('SELECT participant_name FROM participants')
            participants = cursor.fetchall()

    except Exception as e:
        print(f"エラー: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('group.html', groups=groups, participants=participants)