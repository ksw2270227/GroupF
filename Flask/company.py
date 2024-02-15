from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

company_bp = Blueprint('company', __name__)

# データベースとの接続を確立する関数
def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@company_bp.route('/save_company_info', methods=['POST'])
def save_company_info():
    if request.method == 'POST':
        company_id = request.form['company_id']
        company_name = request.form['company_name']
        company_password = request.form['company_password']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']

        # データベースに接続
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # ユーザー情報をusersテーブルに挿入
            cursor.execute('INSERT INTO users (company_id, company_name, company_password, address, phone_number, email_address) VALUES (?, ?, ?, ?, ?, ?)',
                            (company_id, company_name, company_password, address, phone_number, email_address))
            conn.commit()
            message = "企業情報が正常に保存されました。"
        except Exception as e:
            conn.rollback()
            message = f"エラーが発生しました: {str(e)}"
        finally:
            cursor.close()
            conn.close()

        return render_template('company_response.html', message=message)

# エラーページのハンドラ
@company_bp.route('/error')
def error():
    return render_template('error.html', error_message='リクエストを処理できませんでした。')

