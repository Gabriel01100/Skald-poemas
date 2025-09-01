from flask import render_template, request, redirect, url_for, session, current_app
from . import bp
from werkzeug.security import check_password_hash


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        contrasena = request.form['contrasena'].strip()

        resultado = check_password_hash(current_app.config['ADMIN_PASSWORD_HASH'], contrasena)

        if usuario == current_app.config['ADMIN_USER'] and resultado:
            print("Login exitoso")
            session['usuario'] = usuario
            return redirect(url_for('poemas.agregar'))

        print("Login fallido")
        return render_template('auth/login.html', error='Credenciales incorrectas')
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('poemas.login'))