from flask_restful import Resource, fields, marshal_with, abort
from flask import request
from . import api
from models import db, Juego

# Qué campos del objeto Juego salen en el JSON
juego_fields = {
    "id": fields.Integer,
    "nombre": fields.String,
    "descripcion": fields.String,
    "precio": fields.Float,
}


def validar_datos(data):
    """Valida el JSON recibido. Regresa (nombre, descripcion, precio) o aborta con 400."""
    if not isinstance(data, dict):
        abort(400, message="Se esperaba un JSON con nombre, descripcion y precio.")

    faltan = [c for c in ("nombre", "descripcion", "precio") if c not in data]
    if faltan:
        abort(400, message=f"Faltan campos: {', '.join(faltan)}")

    nombre = data["nombre"]
    descripcion = data["descripcion"]
    precio = data["precio"]

    if not isinstance(nombre, str) or not nombre.strip():
        abort(400, message="'nombre' debe ser texto no vacío.")
    if not isinstance(descripcion, str) or not descripcion.strip():
        abort(400, message="'descripcion' debe ser texto no vacío.")
    # bool es subclase de int en Python, por eso se excluye aparte
    if isinstance(precio, bool) or not isinstance(precio, (int, float)) or precio < 0:
        abort(400, message="'precio' debe ser un número mayor o igual a 0.")

    return nombre.strip(), descripcion.strip(), float(precio)


def obtener_o_404(id):
    juego = db.session.get(Juego, id)
    if juego is None:
        abort(404, message=f"No existe el juego con id {id}")
    return juego


class JuegoList(Resource):
    @marshal_with(juego_fields)
    def get(self):
        """GET /api/juegos
        Devuelve la lista de todos los juegos. 200 OK."""
        return Juego.query.all(), 200

    @marshal_with(juego_fields)
    def post(self):
        """POST /api/juegos
        Crea un juego. Body JSON: {nombre, descripcion, precio}.
        201 Created con el juego creado; 400 si el JSON es inválido."""
        data = request.get_json(silent=True)
        nombre, descripcion, precio = validar_datos(data)
        juego = Juego(nombre=nombre, descripcion=descripcion, precio=precio)
        db.session.add(juego)
        db.session.commit()
        return juego, 201


class JuegoResource(Resource):
    @marshal_with(juego_fields)
    def get(self, id):
        """GET /api/juegos/<id>
        Devuelve un juego. 200 OK; 404 si no existe."""
        return obtener_o_404(id), 200

    @marshal_with(juego_fields)
    def put(self, id):
        """PUT /api/juegos/<id>
        Reemplaza los datos de un juego. Body JSON: {nombre, descripcion, precio}.
        200 OK; 400 si el JSON es inválido; 404 si no existe."""
        juego = obtener_o_404(id)
        nombre, descripcion, precio = validar_datos(request.get_json(silent=True))
        juego.nombre = nombre
        juego.descripcion = descripcion
        juego.precio = precio
        db.session.commit()
        return juego, 200

    def delete(self, id):
        """DELETE /api/juegos/<id>
        Elimina un juego. 204 No Content; 404 si no existe."""
        juego = obtener_o_404(id)
        db.session.delete(juego)
        db.session.commit()
        return "", 204


api.add_resource(JuegoList, "/juegos")
api.add_resource(JuegoResource, "/juegos/<int:id>")