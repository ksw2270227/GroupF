from flask import Flask,render_template
from testIndex import testIndex_bp
from index import index_bp
from docker_mysql import docker_mysql_bp
from register import register_bp
from signup import signup_bp
from chat import chat_bp
from creategroup import creategroup_bp
from mypage import mypage_bp

app = Flask(__name__)
app.register_blueprint(testIndex_bp)
app.register_blueprint(index_bp)
app.register_blueprint(docker_mysql_bp)
app.register_blueprint(register_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(creategroup_bp)
app.register_blueprint(mypage_bp)


@app.route("/")
def show_urls():
    urls = [{"rule": rule.rule, "endpoint": rule.endpoint} for rule in app.url_map.iter_rules()]
    return render_template('list_urls.html', urls=urls)

if __name__ == "__main__":
    app.run()  # あるいは任意のポート

print("ok")