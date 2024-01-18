from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3

mypage_bp = Blueprint('mypage', __name__)

def get_db_connection():
    # SQLiteデータベースに接続するための関数
    conn = sqlite3.connect('testDB.db')
    return conn

@mypage_bp.route('/mypage')
def mypage():
    # セッションからユーザーIDを取得
    user_id = session.get('user_id')

    if not user_id:
        # ユーザーがログインしていない場合はログインページにリダイレクトkkk
        print("ログインしてない")
        return redirect(url_for('index.index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # ユーザーIDを使用してユーザーの情報を取得
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user_info = cursor.fetchone()

        if user_info:
            # マイページにユーザー情報を渡して表示
            print("たから")
            print(user_info)
            return render_template('mypage.html', user_info=user_info)
        else:
            # ユーザー情報が見つからない場合はエラーを表示
            return render_template('error.html', message='ユーザー情報が見つかりません。')

    except Exception as e:
        # エラーが発生した場合はエラーページを表示
        # return render_template('error.html', message=str(e))
        print(e)
        print("なんかエラーでた")
        return redirect(url_for('index.index'))

    finally:
        cursor.close()
        conn.close()



