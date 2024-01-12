from flask import Flask
from testIndex import testIndex_bp
from index import index_bp

app = Flask(__name__)
app.register_blueprint(testIndex_bp)
app.register_blueprint(index_bp)

@app.route("/")
def show_urls():
    urls = [rule.rule for rule in app.url_map.iter_rules()]
    # HTMLリストとしてフォーマット
    return '<ul>' + ''.join([f'<li>{url}</li>' for url in urls]) + '</ul>'

if __name__ == "__main__":
    app.run()  # あるいは任意のポート

print("ok")