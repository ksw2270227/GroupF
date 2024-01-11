from flask import Blueprint

testIndex_bp = Blueprint('testIndex',__name__)

@testIndex_bp.route("/testIndex")
def index():
    return "<h1>(カッコ)一旦これで</h1>"