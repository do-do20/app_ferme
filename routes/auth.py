from flask import Blueprint, request, jsonify
from database import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM utilisateur WHERE email=%s AND password=%s",
                   (data['email'], data['password']))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"success": True, "user": user})
    else:
        return jsonify({"success": False})