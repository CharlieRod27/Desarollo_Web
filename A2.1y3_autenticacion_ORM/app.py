from flask import Flask, render_template, request, redirect
from models import db, login_manager
from auth import auth_bp
import controlador_juegos
from flask_login import login_required

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://Pokecharlie:root@localhost/juegos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "todavia-esta-contaseña"

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"        # a dónde mandar a quien no ha iniciado sesión
login_manager.login_message = "Inicia sesión para ver esta página."

app.register_blueprint(auth_bp, url_prefix="/auth")






@app.route("/")
def inicio():
    return redirect("/juegos")

@app.route("/juegos")
@login_required
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    return redirect("/juegos")

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form["id"])
    return redirect("/juegos")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8000)