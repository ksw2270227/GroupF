from flask import Flask, render_template, jsonify, Blueprint
import mysql.connector

check_data_bp = Blueprint('check_data', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@check_data_bp.route('/check_data')
def check_data():
    return render_template('check_data.html')

@check_data_bp.route('/get_table_data/<table_name>')
def get_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    allowed_tables = ['users', 'admins', 'companies', 'groups', 'events', 'messages', 'location_data', 'location_history']
    if table_name not in allowed_tables:
        return jsonify({'error': 'Invalid table name'}), 400

    try:
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# FlaskアプリケーションでBlueprintを登録
# app.register_blueprint(check_data_bp, url_prefix='/data')
