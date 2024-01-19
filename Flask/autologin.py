# login.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash,jsonify
import sqlite3

auto_login_bp = Blueprint('auto_login', __name__)

@auto_login_bp.route("/auto-login", methods=["POST"])
def auto_login():
    # 通常はここでユーザー認証を行いますが、デモのために固定値を使用
    session['user_id'] = 1
    session['user_name'] = 'hanako@example.com'
    return jsonify({"message": "Logged in successfully", "user_id": 1, "user_name": 'hanako@example.com'})
