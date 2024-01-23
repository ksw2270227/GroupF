from flask import Blueprint, render_template
import sqlite3

group_bp = Blueprint('group', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@group_bp.route('/group/<int:group_id>')
def view_group(group_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # グループ情報の取得
    cursor.execute('SELECT * FROM groups WHERE group_id = ?', (group_id,))
    group = cursor.fetchone()

    if group:
        # グループの参加者情報の取得
        cursor.execute('SELECT full_name FROM users WHERE current_group_id = ?', (group_id,))
        participants = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('group.html', group=group, participants=participants)
    else:
        cursor.close()
        conn.close()
        return render_template('error.html', error_message='指定されたグループは存在しません')