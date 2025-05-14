# app.py
from flask import Flask
from poemas.routes import bp

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
