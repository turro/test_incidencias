from flask import Flask, request, render_template
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

# Base de datos (se podría utilizar un sistema más robusto en producción)
DATABASE = 'incidencias.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')  # El archivo HTML debe estar en la carpeta "templates"

@app.route('/report', methods=['POST'])
def report():
    service = request.form['service']
    description = request.form['description'] if service == 'otro' else ''
    timestamp = datetime.now()

    conn = get_db_connection()
    conn.execute('INSERT INTO incidencias (service, description, timestamp) VALUES (?, ?, ?)',
                 (service, description, timestamp))
    conn.commit()
    conn.close()
    
    return 'Incidencia reportada con éxito. ¡Gracias!'

@app.route('/incidencias')
def incidencias():
    # Obtiene todas las incidencias en la última hora
    time_threshold = datetime.now() - timedelta(hours=1)
    conn = get_db_connection()
    incidencias = conn.execute('SELECT * FROM incidencias WHERE timestamp > ?', (time_threshold,)).fetchall()
    conn.close()
    
    return render_template('incidencias.html', incidencias=incidencias)  # Necesitarás un archivo HTML para esto también

if __name__ == '__main__':
    app.run(debug=True)
