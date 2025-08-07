# poemas/models.py
import sqlite3
from datetime import datetime
from flask import current_app

def conectar_bd():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def agregar_poema(titulo, contenido, etiquetas, fecha):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("INSERT INTO poemas (titulo, contenido, etiquetas, fecha) VALUES (?, ?, ?, ?)",
                (titulo, contenido, etiquetas, fecha))
    conn.commit()
    conn.close()

def obtener_poemas():
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT * FROM poemas ORDER BY id DESC")
    poemas = cur.fetchall()
    conn.close()
    return poemas

def eliminar_poema_por_id(id):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("DELETE FROM poemas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
