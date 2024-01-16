from flask import Flask, render_template, request, redirect, url_for, Blueprint
import mysql.connector

creategroup_bp = Blueprint('creategroup', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@creategroup_bp.route('/creategroup', methods=['GET', 'POST'])
def create_group():
    if request.method == 'GET':
        return render_template("creategroup.html")

    if request.method == 'POST':
        group_name = request.form['group_name']
        password = request.form['password']
        user_id = request.form['user_id']
        max_members = request.form['max_members']
        # Other form fields...

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Insert data into the users table
            cursor.execute('INSERT INTO users (group_name, password, user_id, max_members) VALUES (%s, %s, %s, %s)',
                           (group_name, password, user_id, max_members))
            conn.commit()

            # Optionally, you can do further processing or redirect to another page upon success
            return redirect(url_for('index'))  # Redirect to the index page after successful insertion

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            # Handle the error, display a message, or redirect to an error page

        finally:
            cursor.close()
            conn.close()

    # Handle other HTTP methods or render the creategroup.html template
    return render_template('creategroup.html')
