from flask import Blueprint, render_template
import sqlite3

group_bp = Blueprint('group', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@group_bp.route('/group', defaults={'group_id': None})
def view_group(group_id):
    if group_id is not None:
        try:
            group_id = int(group_id)
        except ValueError:
            return render_template('group.html', error_message='グループIDは整数である必要があります')

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
            return render_template('group.html', error_message='指定されたグループは存在しません')
    else:
        # 全グループ情報の取得（いったん省略）
        return render_template('group.html')
