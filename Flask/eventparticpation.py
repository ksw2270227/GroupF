from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask import jsonify


eventparticpation_bp = Blueprint('eventparticpation', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@eventparticpation_bp.route('/eventparticpation', methods=['GET', 'POST'])
def eventparticpation():
    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = session.get('user_id')
    
    

    # ログインしていればeventparticpationを表示
    if user_id is None:
        return redirect(url_for('login.login_user'))
    elif user_id:
        # ユーザーのcurrent_group_idを取得
        cursor.execute('SELECT current_event_id FROM users WHERE user_id = ?', (user_id,))
        current_event_id =cursor.fetchone()[0]
        if current_event_id > 0:
            return redirect(url_for('event.event'))
        else:
            return render_template("eventparticpation.html")