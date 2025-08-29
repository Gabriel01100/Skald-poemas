from flask import render_template, request, redirect, url_for, session
from . import bp
from ..models import agregar_poema, obtener_poemas, eliminar_poema_por_id
from datetime import datetime
import sqlite3


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
    return render_template('admin/agregar.html', poemas=poemas)

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

    return render_template('admin/editar.html', poema=poema)
