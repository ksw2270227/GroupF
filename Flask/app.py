from flask import Flask,render_template,session
from index import index_bp
from register import register_bp
from signup import signup_bp
from chat import chat_bp
from creategroup import creategroup_bp
from check_data import check_data_bp
from group import group_bp
from create_SQLite_DB import create_SQLite_DB_bp
from login import login_bp
from mypage import mypage_bp
from map import map_bp
from joingroup import joingroup_bp
from logout import logout_bp
from autologin import auto_login_bp
from selectchatpartner import selectchatpartner_bp

app = Flask(__name__)
app.register_blueprint(index_bp)
app.register_blueprint(register_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(selectchatpartner_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(creategroup_bp)
app.register_blueprint(check_data_bp)
app.register_blueprint(group_bp)
app.register_blueprint(create_SQLite_DB_bp)
app.register_blueprint(login_bp)
app.register_blueprint(mypage_bp)
app.register_blueprint(map_bp)
app.register_blueprint(joingroup_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(auto_login_bp)

try:
    with open('Flask/secret_key.txt', 'r') as file:
        app.secret_key = file.read().strip()
    print("Secret Key set to:", app.secret_key)
except Exception as e:
    print("Error reading secret key file:", e)


@app.route("/")
def show_urls():
    urls = [{"rule": rule.rule, "endpoint": rule.endpoint} for rule in app.url_map.iter_rules()]
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    return render_template('list_urls.html', urls=urls, user_name=user_name, user_id=user_id)


if __name__ == "__main__":
    app.run()  # あるいは任意のポート.
