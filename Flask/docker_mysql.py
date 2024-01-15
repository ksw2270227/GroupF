from flask import Flask, render_template
import mysql.connector
from flask import Blueprint
docker_mysql_bp = Blueprint('docker_mysql',__name__)


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@docker_mysql_bp.route('/docker_mysql')
def show_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('docker_mysql.html', users=users)

