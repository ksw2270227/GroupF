from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask import Blueprint

signup_bp = Blueprint('signup', __name__)

import sqlite3

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@signup_bp.route('/signup', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # 以下のフォームデータ取得部分は変更不要
        user_name = request.form['user_name'][:10]
        full_name = request.form['full_name'][:20]
        phone_number = request.form['phone_number'][:15]
        email_address = request.form['email_address'][:254]
        password = request.form['password'][:40]
        age = request.form['age'][:3]
        gender = request.form['gender']

        conn = get_db_connection()
        cursor = conn.cursor()


        cursor.execute(
            'INSERT INTO users (user_name, full_name, phone_number, email_address, password, age, gender) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_name, full_name, phone_number, email_address, password, age, gender)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index.index'))
    
    return render_template('signup.html')
