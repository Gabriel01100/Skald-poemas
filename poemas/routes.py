'''

# poemas/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from datetime import datetime
from werkzeug.security import check_password_hash
from .models import agregar_poema, obtener_poemas, eliminar_poema_por_id
import sqlite3

bp = Blueprint('poemas', __name__)

#Ruta principal 
@bp.route('/')
def index():
    poemas = obtener_poemas()
    return render_template('index.html', poemas=poemas)

#'Mas poemas' Ruta donde van a visualizar todos los poemas disponibles
@bp.route('/more')
def more():
    etiqueta_filtro = request.args.get('etiqueta')
    todos_poemas = obtener_poemas() 

    # Extraer etiquetas válidas desde TODOS los poemas
    etiquetas_conteo = {}
    for p in todos_poemas:
        if p["etiquetas"]:
            for e in [e.strip() for e in p["etiquetas"].split(",")]:
                etiquetas_conteo[e] = etiquetas_conteo.get(e, 0) + 1

    etiquetas = sorted(etiquetas_conteo.keys())

    # filtro la lista que se muestra
    if etiqueta_filtro:
        poemas = [
            p for p in todos_poemas 
            if etiqueta_filtro in [e.strip() for e in (p["etiquetas"] or "").split(",")]
        ]
    else:
        poemas = todos_poemas

    return render_template("more.html", poemas=poemas, etiquetas=etiquetas)

#Mostrar los poemas sin recargar la pagian
@bp.route('/filtrar')
def filtrar():
    etiqueta = request.args.get('etiqueta')
    poemas = obtener_poemas()

    if etiqueta:
        poemas = [p for p in poemas if etiqueta in [e.strip() for e in (p['etiquetas'] or '').split(',')]]


    return render_template('fragmentos/poemas.html', poemas=poemas)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        contrasena = request.form['contrasena'].strip()

        resultado = check_password_hash(current_app.config['ADMIN_PASSWORD_HASH'], contrasena)
        print("¿Coincide el hash con la contraseña?", resultado)

        if usuario == current_app.config['ADMIN_USER'] and resultado:
            print("Login exitoso")
            session['usuario'] = usuario
            return redirect(url_for('poemas.agregar'))

        print("Login fallido")
        return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')

    

@bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('poemas.login'))

@bp.route('/admin/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario' not in session:
        return redirect(url_for('poemas.login'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        etiquetas = request.form['etiquetas']

        etiquetas = ",".join([e.strip() for e in etiquetas.split(",")])

        fecha = datetime.now().strftime('%Y-%m-%d')

        agregar_poema(titulo, contenido, etiquetas, fecha)
        return redirect(url_for('poemas.agregar'))

    poemas = obtener_poemas()
    return render_template('agregar.html', poemas=poemas)

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    if 'usuario' not in session:
        return redirect(url_for('poemas.login'))

    eliminar_poema_por_id(id)
    return redirect(url_for('poemas.agregar'))

@bp.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' not in session:
        return redirect(url_for('poemas.login'))

    conn = sqlite3.connect("poemas.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        etiquetas = request.form['etiquetas']
        etiquetas = ",".join([e.strip() for e in etiquetas.split(",")])

        cur.execute("""
            UPDATE poemas
            SET titulo = ?, contenido = ?, etiquetas = ?
            WHERE id = ?
        """, (titulo, contenido, etiquetas, id))
        conn.commit()
        conn.close()
        return redirect(url_for('poemas.agregar'))
    
    # Método GET: obtener datos del poema a editar
    cur.execute("SELECT * FROM poemas WHERE id = ?", (id,))
    poema = cur.fetchone()
    conn.close()

    return render_template('editar.html', poema=poema)




'''