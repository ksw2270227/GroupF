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
    if request.method == 'POST':
        # フォームから送信されたデータを取得
        group_name = request.form['group_name']
        group_id = request.form['group_id']
        # 他のフォームフィールドも同様に取得する

        # データベースに接続
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # データベースにデータを挿入
            cursor.execute('INSERT INTO users (group_name, group_id) VALUES (%s, %s)', (group_name, group_id))
            # 他のフォームフィールドも適切に挿入する

            # データベースへの変更を確定
            conn.commit()

            # 成功した場合、リダイレクトなどの適切な処理を行う
            return redirect(url_for('group.create_group'))
        except Exception as e:
            # エラーが発生した場合、ロールバック
            conn.rollback()
            print(f"Error: {e}")

        finally:
            # 接続をクローズ
            cursor.close()
            conn.close()

    # GETメソッドの場合は単にテンプレートを表示
    return render_template('group.html')

# 他の関連するルートや処理を追加することも可能
