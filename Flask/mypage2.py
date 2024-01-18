from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask import Blueprint

mypage_bp = Blueprint('mypage', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='your_database_name',
        user='your_database_user',
        password='your_database_password'
    )

@mypage_bp.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if request.method == 'POST':
        # フォームから送信されたデータを取得
        user_name = request.form['user_name']
        full_name = request.form['full_name']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']
        password = request.form['password']  # 通常、パスワードはハッシュ化して保存するべき

        try:
            # データベースに接続
            conn = get_db_connection()
            cursor = conn.cursor()

            # データベースに新しいユーザーを挿入
            cursor.execute('''
                INSERT INTO users (user_name, full_name, phone_number, email_address, password)
                VALUES (%s, %s, %s, %s, %s)
            ''', (user_name, full_name, phone_number, email_address, password))

            # 変更をコミット
            conn.commit()

            # 接続を閉じる
            cursor.close()
            conn.close()

            # マイページにリダイレクト
            return redirect(url_for('mypage.mypage'))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            # エラーが発生した場合はロールバック
            conn.rollback()

        finally:
            # 接続を確実に閉じる
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template('mypage.html')
