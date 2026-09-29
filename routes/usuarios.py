from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, session
from models.user import User
from forms import RegistrationForm, LoginForm, EditProfileForm

users_bp = Blueprint("users", __name__)

@users_bp.route("/")
def index():
    users = User.get_all()
    return render_template("user_list.html", users=users)

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.get_by_username(form.username.data):
            flash("Ese nombre de usuario ya existe")
        elif User.get_by_email(form.email.data):
            flash("Ese correo ya está registrado")
        else:
            User.create(form.username.data, form.email.data, form.password.data)
            flash("Registro exitoso")
            return redirect(url_for("users.index"))
    return render_template("register.html", form=form)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para ver esa página")
            return redirect(url_for("users.login"))
        return f(*args, **kwargs)
    return wrapper

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user["password"] == form.password.data:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Bienvenido, " + user["username"])
            return redirect(url_for("users.index"))
        flash("Usuario o contraseña incorrectos")
    return render_template("login.html", form=form)


@users_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada")
    return redirect(url_for("users.index"))

@users_bp.route("/profile/<int:id>")
@login_required
def profile(id):
    user = User.get_by_id(id)
    if not user:
        flash("Usuario no encontrado")
        return redirect(url_for("users.index"))
    return render_template("profile.html", user=user)


@users_bp.route("/profile/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(id):
    if session["user_id"] != id:
        flash("Solo puedes editar tu propio perfil")
        return redirect(url_for("users.index"))

    user = User.get_by_id(id)
    form = EditProfileForm(data=user)

    if form.validate_on_submit():
        por_usuario = User.get_by_username(form.username.data)
        por_correo = User.get_by_email(form.email.data)
        if por_usuario and por_usuario["id"] != id:
            flash("Ese nombre de usuario ya existe")
        elif por_correo and por_correo["id"] != id:
            flash("Ese correo ya está registrado")
        else:
            User.update(id, form.username.data, form.email.data)
            session["username"] = form.username.data
            flash("Perfil actualizado")
            return redirect(url_for("users.profile", id=id))

    return render_template("edit_profile.html", form=form, user=user)


@users_bp.route("/profile/<int:id>/delete", methods=["POST"])
@login_required
def delete_profile(id):
    if session["user_id"] != id:
        flash("Solo puedes eliminar tu propia cuenta")
        return redirect(url_for("users.index"))

    User.delete(id)
    session.clear()
    flash("Cuenta eliminada")
    return redirect(url_for("users.index"))