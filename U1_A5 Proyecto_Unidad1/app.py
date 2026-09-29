from flask import Flask
from flask_wtf.csrf import CSRFProtect
from routes.usuarios import users_bp   # busca en la carpeta routes el archivo usuarios.py y toma users_bp
from models import db                  # la instancia de SQLAlchemy que vive en models/__init__.py

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esto-por-algo-largo"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://Pokecharlie:root@localhost/peliculas"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

CSRFProtect(app)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)