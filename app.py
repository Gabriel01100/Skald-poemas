# app.py
from flask import Flask
from poemas.routes import bp
from config import Config
from extensions import mail

app = Flask(__name__)
app.config.from_object(Config)

mail.init_app(app)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
