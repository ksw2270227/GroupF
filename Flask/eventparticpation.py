from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask import jsonify


eventparticpation_bp = Blueprint('eventparticpation', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@eventparticpation_bp.route('/eventparticpation', methods=['GET', 'POST'])
def login_user():

    if request.method == 'POST':
        event_id = request.form['eventidinput']
        password = request.form['passwordinput']
        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザーを検索
        cursor.execute(
            'SELECT * FROM users WHERE event_id = ? AND password = ?',(event_id, password)
        )
        event = cursor.fetchone()
        print(event)

        session['event_id'] = event[0]

        cursor.close()
        conn.close()

        
        return render_template("event.html")
    else :
        return render_template("eventparticpation.html")     