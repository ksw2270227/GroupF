from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from flask import Blueprint

signup_bp = Blueprint('signup', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@signup_bp.route('/signup', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        user_name = request.form['user_name'][:10]
        full_name = request.form['full_name'][:20]
        phone_number = request.form['phone_number'][:15]
        email_address = request.form['email_address'][:254]
        password = request.form['password'][:40]
        age = request.form['age'][:3]
        gender = request.form['gender']

        conn = get_db_connection()
        cursor = conn.cursor()

        # 電話番号またはメールアドレスが既にデータベースに存在するか確認
        cursor.execute(
            'SELECT * FROM users WHERE phone_number = ? OR email_address = ?',
            (phone_number, email_address)
        )
        existing_user = cursor.fetchone()

        if existing_user:
            flash('同じ電話番号またはメールアドレスが既に登録されています。', 'error')
            return render_template('signup.html', form_data=request.form)

        cursor.execute(
            'INSERT INTO users (user_name, full_name, phone_number, email_address, password, age, gender) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_name, full_name, phone_number, email_address, password, age, gender)
        )

        conn.commit()
        cursor.close()
        conn.close()

        flash('ユーザーが正常に登録されました。', 'success')
        return redirect(url_for('index.index'))
    
    return render_template('signup.html')