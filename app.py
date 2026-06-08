from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = "ferme_secret"

# =====================================
# MYSQL CONFIG
# =====================================

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ferme'

mysql = MySQL(app)

# =====================================
# LOGIN PAGE
# =====================================

@app.route('/')
def home():
    return render_template('login.html')

# =====================================
# LOGIN
# =====================================

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""

        SELECT * FROM utilisateur

        WHERE email=%s
        AND password=%s

    """,(email,password))

    user = cursor.fetchone()

    cursor.close()

    if user:

        session['id_user'] = user['id_user']
        session['nom'] = user['nom']

        return jsonify({
            "success": True
        })

    else:

        return jsonify({
            "success": False
        })

# =====================================
# LOGOUT
# =====================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

# =====================================
# =====================================
# =====================================
# DASHBOARD
# =====================================

@app.route('/dashboard')
def dashboard():

    if 'id_user' not in session:
        return redirect('/')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # =====================================
    # TOTAL VACHES
    # =====================================

    cursor.execute("""

        SELECT COUNT(*) as total

        FROM vache

        WHERE id_user=%s

    """,(session['id_user'],))

    total_vaches = cursor.fetchone()['total']

    # =====================================
    # TOTAL PRODUCTION DH
    # =====================================

    cursor.execute("""

        SELECT

        IFNULL(
            SUM(quantite * prix),
            0
        ) as total

        FROM production

        WHERE id_user=%s

    """,(session['id_user'],))

    total_lait = cursor.fetchone()['total']

    # =====================================
    # TOTAL DEPENSE
    # =====================================

    cursor.execute("""

        SELECT

        IFNULL(
            SUM(montant),
            0
        ) as total

        FROM depense

        WHERE id_user=%s

    """,(session['id_user'],))

    total_depense = cursor.fetchone()['total']

    # =====================================
    # VACHES GESTANTES
    # =====================================

    cursor.execute("""

        SELECT *

        FROM vache

        WHERE

        id_user=%s
        AND gestante=1

        ORDER BY date_velage_prevue ASC

    """,(session['id_user'],))

    vaches_gestantes = cursor.fetchall()

    # =====================================
    # STATISTIQUES VACHES
    # =====================================

    cursor.execute("""

        SELECT

            vache.nom,

            IFNULL(
                SUM(production.quantite * production.prix),
                0
            ) as total_production,

            IFNULL(
                SUM(depense.montant),
                0
            ) as total_depense

        FROM vache

        LEFT JOIN production
        ON vache.id_vache = production.id_vache

        LEFT JOIN depense
        ON vache.id_vache = depense.id_vache

        WHERE vache.id_user=%s

        GROUP BY vache.id_vache

    """,(session['id_user'],))

    statistiques_vaches = cursor.fetchall()

    cursor.close()

    return render_template(

        'dashboard.html',

        total_vaches=total_vaches,
        total_lait=total_lait,
        total_depense=total_depense,
        vaches_gestantes=vaches_gestantes,
        statistiques_vaches=statistiques_vaches

    )
# =====================================
# PAGE VACHE
# =====================================

@app.route('/vache')
def vache():

    if 'id_user' not in session:
        return redirect('/')

    return render_template('vache.html')


# =====================================
# GET VACHES
# =====================================

@app.route('/get_vaches')
def get_vaches():

    if 'id_user' not in session:
        return jsonify([])

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""

        SELECT *

        FROM vache

        WHERE id_user=%s

        ORDER BY id_vache DESC

    """,(session['id_user'],))

    data = cursor.fetchall()

    cursor.close()

    return jsonify(data)


# =====================================
# ADD VACHE
# =====================================

@app.route('/add_vache', methods=['POST'])
def add_vache():

    if 'id_user' not in session:
        return jsonify({
            "success": False
        })

    data = request.get_json()

    cursor = mysql.connection.cursor()

    cursor.execute("""

        INSERT INTO vache(

            nom,
            race,
            id_user,
            date_naissance,
            etat,
            date_insemination,
            date_diagnostic,
            gestante,
            date_velage_prevue,
            date_velage,
            nombre_veau

        )

        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

    """,(

        data['nom'],
        data['race'],
        session['id_user'],
        data['date_naissance'],
        data['etat'],
        data['date_insemination'],
        data['date_diagnostic'],
        data['gestante'],
        data['date_velage_prevue'],
        data['date_velage'],
        data['nombre_veau']

    ))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        "success": True
    })


# =====================================
# DELETE VACHE
# =====================================

@app.route('/delete_vache/<int:id>')
def deleteVache(id):

    if 'id_user' not in session:
        return jsonify({
            "success": False
        })

    cursor = mysql.connection.cursor()

    cursor.execute("""

        DELETE FROM vache

        WHERE id_vache=%s
        AND id_user=%s

    """,(id, session['id_user']))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        "success": True
    })


# =====================================
# UPDATE VACHE
# =====================================

@app.route('/update_vache/<int:id>', methods=['POST'])
def update_vache(id):

    if 'id_user' not in session:
        return jsonify({
            "success": False
        })

    data = request.get_json()

    cursor = mysql.connection.cursor()

    cursor.execute("""

        UPDATE vache

        SET

        nom=%s,
        race=%s,
        etat=%s

        WHERE id_vache=%s
        AND id_user=%s

    """,(

        data['nom'],
        data['race'],
        data['etat'],
        id,
        session['id_user']

    ))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        "success": True
    })

# =====================================
# =====================================
# PAGE PRODUCTION
# =====================================

@app.route('/production')
def production():

    if 'id_user' not in session:
        return redirect('/')

    return render_template('production.html')


# =====================================
# GET PRODUCTION
# =====================================

@app.route('/get_production')
def get_production():

    if 'id_user' not in session:
        return jsonify([])

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""

        SELECT

            production.*,
            vache.nom

        FROM production

        LEFT JOIN vache
        ON production.id_vache = vache.id_vache

        WHERE production.id_user=%s

        ORDER BY production.id_production DESC

    """,(session['id_user'],))

    data = cursor.fetchall()

    cursor.close()

    return jsonify(data)


# =====================================
# ADD PRODUCTION
# =====================================

@app.route('/add_production', methods=['POST'])
def add_production():

    if 'id_user' not in session:
        return jsonify({
            "success": False
        })

    data = request.get_json()

    cursor = mysql.connection.cursor()

    cursor.execute("""

        INSERT INTO production(

            date,
            quantite,
            id_vache,
            id_user,
            type,
            prix

        )

        VALUES(%s,%s,%s,%s,%s,%s)

    """,(

        data['date'],
        data['quantite'],
        data['id_vache'],
        session['id_user'],
        data['type'],
        data['prix']

    ))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        "success": True
    })


# =====================================
# DELETE PRODUCTION
# =====================================

@app.route('/delete_production/<int:id>')
def delete_production(id):

    if 'id_user' not in session:
        return jsonify({
            "success": False
        })

    cursor = mysql.connection.cursor()

    cursor.execute("""

        DELETE FROM production

        WHERE id_production=%s
        AND id_user=%s

    """,(id, session['id_user']))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        "success": True
    })


# =====================================
# =====================================
# UPDATE PRODUCTION
# =====================================

@app.route('/update_production/<int:id>', methods=['POST'])
def update_production(id):

    data = request.get_json()

    cursor = mysql.connection.cursor()

    cursor.execute("""

        UPDATE production

        SET

        quantite=%s,
        prix=%s

        WHERE id_production=%s

    """,(

        data['quantite'],
        data['prix'],
        id

    ))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        "success": True
    })

# =====================================
# =====================================
# PAGE DEPENSE
# =====================================

@app.route('/depense')
def depense():

    if 'id_user' not in session:
        return redirect('/')

    return render_template('depense.html')


# =====================================
# GET DEPENSE
# =====================================

@app.route('/get_depense')
def get_depense():

    if 'id_user' not in session:
        return jsonify([])

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""

        SELECT

            depense.*,
            vache.nom

        FROM depense

        LEFT JOIN vache
        ON depense.id_vache = vache.id_vache

        WHERE depense.id_user=%s

        ORDER BY depense.id_depense DESC

    """,(session['id_user'],))

    data = cursor.fetchall()

    cursor.close()

    return jsonify(data)


# =====================================
# ADD DEPENSE
# =====================================

@app.route('/add_depense', methods=['POST'])
def add_depense():

    if 'id_user' not in session:
        return jsonify({
            "success": False
        })

    data = request.get_json()

    cursor = mysql.connection.cursor()

    cursor.execute("""

        INSERT INTO depense(

            type,
            montant,
            date,
            id_user,
            id_vache

        )

        VALUES(%s,%s,%s,%s,%s)

    """,(

        data['type'],
        data['montant'],
        data['date'],
        session['id_user'],
        data['id_vache']

    ))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        "success": True
    })


# =====================================
# DELETE DEPENSE
# =====================================

@app.route('/delete_depense/<int:id>')
def delete_depense(id):

    if 'id_user' not in session:
        return jsonify({
            "success": False
        })

    cursor = mysql.connection.cursor()

    cursor.execute("""

        DELETE FROM depense

        WHERE id_depense=%s
        AND id_user=%s

    """,(id, session['id_user']))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        "success": True
    })


# =====================================
# UPDATE DEPENSE
# =====================================

@app.route('/update_depense/<int:id>', methods=['POST'])
def update_depense(id):

    if 'id_user' not in session:
        return jsonify({
            "success": False
        })

    data = request.get_json()

    cursor = mysql.connection.cursor()

    cursor.execute("""

        UPDATE depense

        SET

        montant=%s

        WHERE id_depense=%s
        AND id_user=%s

    """,(

        data['montant'],
        id,
        session['id_user']

    ))

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        "success": True
    })

# =====================================
# RUN
# =====================================

if __name__ == '__main__':

    app.run(debug=True)