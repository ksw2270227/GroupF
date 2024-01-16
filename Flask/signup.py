from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask import Blueprint

signup_bp = Blueprint('signup', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@signup_bp.route('/signup', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        user_name = request.form['user_name']
        full_name = request.form['full_name']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']

        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザーをINSERT
        cursor.execute(
            'INSERT INTO users (user_name, full_name, phone_number, email_address, password, age, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (user_name, full_name, phone_number, email_address, password, age, gender)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('docker_mysql.show_users'))  # 登録後にユーザー一覧ページにリダイレクト

    return render_template('signup.html')
