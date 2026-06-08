from flask import Blueprint, request, jsonify
from database import get_db_connection

depense_bp = Blueprint('depense', __name__)

# ✅ ADD
@depense_bp.route('/add_depense', methods=['POST'])
def add_depense():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO depense (type, montant, date, id_user)
        VALUES (%s,%s,%s,%s)
    """, (data['type'], data['montant'], data['date'], data['id_user']))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "added"})


# ✅ GET
@depense_bp.route('/get_depense/<int:id_user>')
def get_depense(id_user):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM depense WHERE id_user=%s", (id_user,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)


# ✅ DELETE
@depense_bp.route('/delete_depense/<int:id>')
def delete_depense(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM depense WHERE id_depense=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "deleted"})


# ✅ UPDATE
@depense_bp.route('/update_depense/<int:id>', methods=['POST'])
def update_depense(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE depense
        SET type=%s, montant=%s, date=%s
        WHERE id_depense=%s
    """, (data['type'], data['montant'], data['date'], id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "updated"})