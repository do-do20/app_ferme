from flask import Blueprint, request, jsonify
from database import get_db_connection

vache_bp = Blueprint('vache', __name__)

# ✅ ADD
@vache_bp.route('/add_vache', methods=['POST'])
def add_vache():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vache (nom, race, age, etat_sante, id_user)
        VALUES (%s,%s,%s,%s,%s)
    """, (data['nom'], data['race'], data['age'], data['etat_sante'], data['id_user']))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "added"})


# ✅ GET ALL
@vache_bp.route('/get_vaches/<int:id_user>')
def get_vaches(id_user):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vache WHERE id_user=%s", (id_user,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)


# ✅ DELETE
@vache_bp.route('/delete_vache/<int:id>')
def delete_vache(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM vache WHERE id_vache=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "deleted"})


# ✅ UPDATE
@vache_bp.route('/update_vache/<int:id>', methods=['POST'])
def update_vache(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE vache 
        SET nom=%s, race=%s, age=%s, etat_sante=%s
        WHERE id_vache=%s
    """, (data['nom'], data['race'], data['age'], data['etat_sante'], id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "updated"})