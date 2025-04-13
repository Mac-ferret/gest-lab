from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connessione al DB
def get_db_connection():
    conn = sqlite3.connect('fascicoli.db')
    conn.row_factory = sqlite3.Row
    return conn

# 👉 ROUTE PRINCIPALE: REDIRECT a /splash
@app.route('/')
def home():
    return redirect(url_for('splash'))

# 👉 ROUTE PER LO SPLASH SCREEN
@app.route('/splash')
def splash():
    return render_template('splash.html')

# 👉 ROUTE PER LA PAGINA INDEX
@app.route('/index')
def index():
    return render_template('index.html')

# (le altre route per GET/POST/PUT/DELETE fascicoli restano uguali)

# Route per ottenere i fascicoli dal database
@app.route('/fascicoli', methods=['GET'])
def get_fascicoli():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fascicoli')
    fascicoli = cursor.fetchall()
    conn.close()

    # Restituisce i dati come JSON per essere usati dal frontend
    return jsonify([dict(fascicolo) for fascicolo in fascicoli])

# Route per inserire un nuovo fascicolo
@app.route('/fascicoli', methods=['POST'])
def add_fascicolo():
    new_fascicolo = request.get_json()
    numero = new_fascicolo['numero']
    operatore = new_fascicolo['operatore']
    ufficio = new_fascicolo['ufficio']
    oggetto = new_fascicolo['oggetto']
    stato = new_fascicolo['stato']

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO fascicoli (numero, operatore, ufficio, oggetto, stato)
        VALUES (?, ?, ?, ?, ?)
    ''', (numero, operatore, ufficio, oggetto, stato))
    conn.commit()
    conn.close()

    return jsonify(new_fascicolo), 201

# Route per aggiornare un fascicolo
@app.route('/fascicoli/<int:id>', methods=['PUT'])
def update_fascicolo(id):
    updated_fascicolo = request.get_json()
    numero = updated_fascicolo['numero']
    operatore = updated_fascicolo['operatore']
    ufficio = updated_fascicolo['ufficio']
    oggetto = updated_fascicolo['oggetto']
    stato = updated_fascicolo['stato']

    conn = get_db_connection()
    conn.execute('''
        UPDATE fascicoli
        SET numero = ?, operatore = ?, ufficio = ?, oggetto = ?, stato = ?
        WHERE id = ?
    ''', (numero, operatore, ufficio, oggetto, stato, id))
    conn.commit()
    conn.close()

    return jsonify(updated_fascicolo)

# Route per eliminare un fascicolo
@app.route('/fascicoli/<int:id>', methods=['DELETE'])
def delete_fascicolo(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM fascicoli WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)