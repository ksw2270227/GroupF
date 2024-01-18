from flask import Blueprint, render_template, session, jsonify,request

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        # ログアウト時にセッションからユーザー情報を削除
        session.pop('user_id', None)
        return jsonify({"success": True})
    return render_template('logout.html')
