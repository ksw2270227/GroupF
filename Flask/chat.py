from flask import Flask,render_template
from testIndex import testIndex_bp
from index import index_bp
from docker_mysql import docker_mysql_bp

chat = Flask(__name__)
chat.register_blueprint(testIndex_bp)
chat.register_blueprint(index_bp)
chat.register_blueprint(docker_mysql_bp)

@chat.route("/chat")
def selectchatpartner():
    
    return render_template('chat.html', urls=urls)

if __name__ == "__main__":
    chat.run()  # あるいは任意のポート

print("ok")