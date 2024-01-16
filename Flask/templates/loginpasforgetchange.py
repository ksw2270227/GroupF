from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='your_database_name',
        user='your_database_user',
        password='your_database_password'
    )

@app.route('/loginpasforgetchange', methods=['POST'])
def loginpasforgetchange():
    if request.method == 'POST':
        # フォームから送信されたデータを取得
        new_password = request.form['nawPasswordInput']
        confirmation_password = request.form['confirmationInput']

        # パスワードが一致しない場合はエラーメッセージを表示
        if new_password != confirmation_password:
            return render_template('loginpasforgetchange.html', error_message='パスワードが一致しません')

        # データベースに接続して新しいパスワードをusersテーブルに挿入
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # パスワードのハッシュ化やセキュリティ対策は実際のプロダクションコードに追加する必要があります
            cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (new_password, 'user_id_here'))

            conn.commit()
            cursor.close()
            conn.close()

            return render_template('success.html')  # パスワード変更成功のページにリダイレクトするか、適切なページに遷移させる

        except Exception as e:
            print(f"Error: {e}")
            return render_template('loginpasforgetchange.html', error_message='パスワード変更に失敗しました')

if __name__ == "__main__":
    app.run(debug=True)
