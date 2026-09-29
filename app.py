from flask import Flask
from flask_wtf.csrf import CSRFProtect
from routes.usuarios import users_bp
##from routes.notes: Le dice a Python que busque dentro de la carpeta routes el archivo llamado usuarios.py.
##import notes_bp: Extrae únicamente la variable notes_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esto-por-algo-largo"

CSRFProtect(app)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)