from models.db import obtener_conexion

class User:

    @staticmethod
    def get_all():
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id, username, email FROM users")
                return cursor.fetchall()
        finally:
            conexion.close()

    @staticmethod
    def create(username, email, password):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, password),
                )
            conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def get_by_username(username):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def get_by_email(email):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def get_by_id(id):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (id,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def update(id, username, email):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET username = %s, email = %s WHERE id = %s",
                    (username, email, id),
                )
            conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def delete(id):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            conexion.commit()
        finally:
            conexion.close()