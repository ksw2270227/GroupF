from flask import Blueprint, render_template, session, request, jsonify
import sqlite3
import datetime

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
            # ユーザーの位置情報が存在する場合
            return render_template('map.html', latitude=location[0], longitude=location[1])
    
    # ユーザーの位置情報が存在しない場合、デフォルトの位置を使用
    return render_template('map.html', latitude=-34.397, longitude=150.644)

# 既存の関数とコード...

@map_bp.route('/api/update-location', methods=['POST'])
def update_location():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    altitude = data.get('altitude', 0)  # デフォルト値は0
    acquisition_time = datetime.datetime.now()  # 現在の時刻を取得

    # データベース接続
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # users テーブルからユーザーステータスを取得
        cursor.execute('SELECT user_status FROM users WHERE user_id = ?', (user_id,))
        user_status_result = cursor.fetchone()
        user_status = user_status_result[0] if user_status_result else 'unknown'

        # location_data テーブルの更新
        cursor.execute('''
            INSERT INTO location_data (user_id, user_status, current_latitude, current_longitude, current_altitude, acquisition_time)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
            user_status = excluded.user_status,
            current_latitude = excluded.current_latitude,
            current_longitude = excluded.current_longitude,
            current_altitude = excluded.current_altitude,
            acquisition_time = excluded.acquisition_time;
        ''', (user_id, user_status, latitude, longitude, altitude, acquisition_time))

        # location_history テーブルへの挿入
        cursor.execute('''
            INSERT INTO location_history (user_id, latitude, longitude, altitude, acquisition_time, user_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, latitude, longitude, altitude, acquisition_time, user_status))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cursor.close()
    conn.close()
    return jsonify({'message': 'Location updated successfully'})