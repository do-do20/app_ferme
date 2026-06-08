from flask import Blueprint, request, jsonify
from database import get_db_connection

production_bp = Blueprint('production', __name__)

# ✅ ADD
@production_bp.route('/add_production', methods=['POST'])
def add_production():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO production (quantite, date, id_vache, id_user)
        VALUES (%s,%s,%s,%s)
    """, (data['quantite'], data['date'], data['id_vache'], data['id_user']))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "added"})


# ✅ GET ALL
@production_bp.route('/get_production/<int:id_user>')
def get_production(id_user):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT production.*, vache.nom 
        FROM production
        JOIN vache ON production.id_vache = vache.id_vache
        WHERE production.id_user=%s
    """, (id_user,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)


# ✅ DELETE
@production_bp.route('/delete_production/<int:id>')
def delete_production(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM production WHERE id_production=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "deleted"})


# ✅ UPDATE
@production_bp.route('/update_production/<int:id>', methods=['POST'])
def update_production(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE production 
        SET quantite=%s, date=%s, id_vache=%s
        WHERE id_production=%s
    """, (data['quantite'], data['date'], data['id_vache'], id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "updated"})