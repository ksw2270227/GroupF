from flask import Flask, render_template, request, redirect, url_for, Blueprint
import sqlite3

joingroup_bp = Blueprint('joingroup', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@joingroup_bp.route('/joingroup', methods=['GET', 'POST'])
def join_group():
    if request.method == 'POST':
        # フォームからグループ参加情報を取得
        group_id = request.form['group_id']
        password = request.form['password']

        # ここでグループIDとパスワードのチェックを行う
        # (仮)IDが"exampleID" パスワードが"examplePass"
        if group_id != "group_id" or password != "password":
            error_message = 'グループIDまたはパスワードが間違っています'
            return render_template('joingroup.html', error_message=error_message)

        # ここで何かしらの処理を行うか、遷移先にデータを送信する処理を記述

        return redirect(url_for('index.index'))
    
    return render_template('joingroup.html')
