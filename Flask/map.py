from flask import Blueprint, render_template, session
import sqlite3

map_bp = Blueprint('map', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@map_bp.route('/map')
def show_map():
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT current_latitude, current_longitude FROM location_data WHERE user_id = ?', (user_id,))
        location = cursor.fetchone()
        cursor.close()
        conn.close()
        if location:
            return render_template('map.html', latitude=location[0], longitude=location[1])
    return render_template('map.html', latitude=-34.397, longitude=150.644)  # デフォルトの位置
