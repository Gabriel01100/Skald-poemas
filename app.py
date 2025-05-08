from flask import Flask, render_template,request, redirect, url_for, session
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/')
def index():
    conn = sqlite3.connect("poemas.db")
    conn.row_factory = sqlite3.Row  # Esto permite acceder a los resultados como diccionarios
    cur = conn.cursor()
    cur.execute("SELECT * FROM poemas ORDER BY id DESC")
    poemas = cur.fetchall()
    conn.close()
    return render_template('index.html', poemas=poemas)

@app.route('/more')
def more():
    etiqueta_filtro = request.args.get('etiqueta')

    conn = sqlite3.connect("poemas.db")
    conn.row_factory = sqlite3.Row  # Esto permite acceder a los resultados como diccionarios
    cur = conn.cursor()
    cur.execute("SELECT * FROM poemas ORDER BY id DESC")
    poemas = cur.fetchall()
    
    #return render_template('more.html', poemas=poemas)

    #Extraer todas las etiquetas (antes del filtro)
    etiquetas = set()
    for p in poemas:
        if p["etiquetas"]:
            etiquetas.update([e.strip() for e in p["etiquetas"].split(",")])

    #Aplicar filtro solo a la lista de poemas mostrados
    if etiqueta_filtro:
        poemas = [p for p in poemas if etiqueta_filtro in [e.strip() for e in (p["etiquetas"] or "").split(",")]]
    else:
        poemas = poemas
    
    conn.close()
    return render_template("more.html", poemas=poemas, etiquetas=sorted(etiquetas))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        # Cambiá estos valores por los que quieras usar
        if usuario == 'admin' and contraseña == '1234':
            session['usuario'] = usuario
            return redirect(url_for('agregar'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


#CRUD DB

def agregar_poema(titulo, contenido, etiquetas, fecha):
    conn = sqlite3.connect('poemas.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO poemas (titulo, contenido, etiquetas, fecha) VALUES (?,?,?,?)", (titulo, contenido, etiquetas, fecha))
    conn.commit()
    conn.close()


@app.route('/admin/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        etiquetas = request.form['etiquetas']
        fecha = datetime.now().strftime('%Y-%m-%d')

        agregar_poema(titulo, contenido, etiquetas, fecha)
        return redirect(url_for('agregar'))
    
    
    #Ver poemas en el admin
    conn = sqlite3.connect("poemas.db")
    conn.row_factory = sqlite3.Row  # Esto permite acceder a los resultados como diccionarios
    cur = conn.cursor()
    cur.execute("SELECT * FROM poemas ORDER BY id DESC")
    poemas = cur.fetchall()
    conn.close()
    
    return render_template('agregar.html', poemas=poemas)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_poema(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect("poemas.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM poemas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('agregar'))



if __name__ == '__main__':
    app.run(debug=True)

