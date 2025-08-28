from flask import render_template, request, redirect, url_for, session, current_app, flash
from flask_mail import Message
from extensions import mail
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


@bp.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method=="POST":
        name = request.form.get("name")
        email = request.form.get('email')
        msj = request.form.get('msj')

        msg = Message(subject=f"Mensaje de {name}", sender=email, recipients=['ggabrielmmiranda.20@gmail.com'])
        msg.body= f"""De: {name} <{email}> 
        Mensaje: {msj}
        """
        msg.reply_to = email  # así podés responderle directo

        try:
            mail.send(msg)
            flash("¡Tu mensaje fue enviado con éxito!", "success")
        except Exception as e:
            flash("Hubo un error al enviar el mensaje", "danger")
            print("Error:", e)

        return redirect(url_for("poemas.contact"))

    return render_template("public/contact.html")


