from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from routes.usuarios import users_bp
from models import db
from models.user import User

app = Flask(__name__)

app.config["SECRET_KEY"] = "un-texto-largo-y-dificil-de-adivinar"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:luna12@localhost/peliculas"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.login_message = "Inicia sesión para ver esta página"


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@app.errorhandler(401)
def error_401(e):
    return render_template("401.html"), 401


@app.errorhandler(403)
def error_403(e):
    return render_template("403.html"), 403


app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)