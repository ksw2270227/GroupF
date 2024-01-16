from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL接続情報
db_config = {
    'host': 'localhost',
    'database': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password'
}

def insert_event(event_name, start_time, end_time, location, event_content):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # イベント情報をINSERT
    insert_query = """
        INSERT INTO event (event_name, start_time, end_time, location, event_content)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = (event_name, start_time, end_time, location, event_content)
    cursor.execute(insert_query, data)

    connection.commit()
    cursor.close()
    connection.close()

@app.route('/submit_event', methods=['POST'])
def submit_event():
    if request.method == 'POST':
        # フォームからデータを取得
        event_name = request.form['event_name']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        location = request.form['location']
        event_content = request.form['event_content']

        # データベースにイベント情報を挿入
        insert_event(event_name, start_time, end_time, location, event_content)

        return redirect(url_for('show_events'))

@app.route('/show_events')
def show_events():
    # データベースからイベント一覧を取得
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    select_query = "SELECT * FROM event"
    cursor.execute(select_query)
    events = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('eventlist.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)
