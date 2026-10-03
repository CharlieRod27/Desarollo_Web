from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from forms import RegistrationForm, LoginForm, EditProfileForm

users_bp = Blueprint("users", __name__)


@users_bp.route("/")
def index():
    return render_template("user_list.html", users=User.get_all())


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.get_by_username(form.username.data):
            flash("Ese nombre de usuario ya existe")
        elif User.get_by_email(form.email.data):
            flash("Ese correo ya está registrado")
        else:
            User.create(form.username.data, form.email.data,
                        generate_password_hash(form.password.data))
            flash("Registro exitoso")
            return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Bienvenido, " + user.username)
            return redirect(url_for("users.index"))
        flash("Credenciales inválidas")
    return render_template("login.html", form=form)


@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada")
    return redirect(url_for("users.index"))


@users_bp.route("/profile")
@login_required
def my_profile():
    return "Hola, " + current_user.username


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
    if current_user.id != id:
        abort(403)
    user = User.get_by_id(id)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        por_usuario = User.get_by_username(form.username.data)
        por_correo = User.get_by_email(form.email.data)
        if por_usuario and por_usuario.id != id:
            flash("Ese nombre de usuario ya existe")
        elif por_correo and por_correo.id != id:
            flash("Ese correo ya está registrado")
        else:
            User.update(id, form.username.data, form.email.data)
            flash("Perfil actualizado")
            return redirect(url_for("users.profile", id=id))
    return render_template("edit_profile.html", form=form, user=user)


@users_bp.route("/profile/<int:id>/delete", methods=["POST"])
@login_required
def delete_profile(id):
    if current_user.id != id:
        abort(403)
    User.delete(id)
    logout_user()
    flash("Cuenta eliminada")
    return redirect(url_for("users.index"))