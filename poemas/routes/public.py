from flask import render_template, request, redirect, url_for, session, current_app
from . import bp
from ..models import obtener_poemas

#Ruta principal 
@bp.route('/')
def index():
    poemas = obtener_poemas()
    return render_template('public/index.html', poemas=poemas)


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

    return render_template("public/more.html", poemas=poemas, etiquetas=etiquetas)

#Mostrar los poemas sin recargar la pagian
@bp.route('/filtrar')
def filtrar():
    etiqueta = request.args.get('etiqueta')
    poemas = obtener_poemas()

    if etiqueta:
        poemas = [p for p in poemas if etiqueta in [e.strip() for e in (p['etiquetas'] or '').split(',')]]


    return render_template('fragmentos/poemas.html', poemas=poemas)
