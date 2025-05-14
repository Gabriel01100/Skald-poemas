# poemas/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from .models import agregar_poema, obtener_poemas, eliminar_poema_por_id

bp = Blueprint('poemas', __name__)

@bp.route('/')
def index():
    poemas = obtener_poemas()
    return render_template('index.html', poemas=poemas)

@bp.route('/more')
def more():
    etiqueta_filtro = request.args.get('etiqueta')
    poemas = obtener_poemas()

    etiquetas = set()
    for p in poemas:
        if p["etiquetas"]:
            etiquetas.update([e.strip() for e in p["etiquetas"].split(",")])

    if etiqueta_filtro:
        poemas = [p for p in poemas if etiqueta_filtro in [e.strip() for e in (p["etiquetas"] or "").split(",")]]

    return render_template("more.html", poemas=poemas, etiquetas=sorted(etiquetas))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        if usuario == 'admin' and contraseña == '1234':
            session['usuario'] = usuario
            return redirect(url_for('poemas.agregar'))
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
