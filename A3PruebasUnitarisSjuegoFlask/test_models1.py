import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app
from models import db, Juego, User


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_crear_juego(self):
        db.session.add(Juego(nombre='Test', descripcion='Desc', precio=9.99))
        db.session.commit()
        self.assertEqual(Juego.query.count(), 1)

    def test_juego_guarda_los_campos(self):
        db.session.add(Juego(nombre='Zelda', descripcion='Aventura', precio=59.9))
        db.session.commit()
        j = Juego.query.filter_by(nombre='Zelda').first()
        self.assertEqual(j.descripcion, 'Aventura')
        self.assertEqual(j.precio, 59.9)

    def test_actualizar_juego(self):
        j = Juego(nombre='Viejo', descripcion='D', precio=1.0)
        db.session.add(j)
        db.session.commit()
        j.nombre = 'Nuevo'
        db.session.commit()
        self.assertEqual(Juego.query.first().nombre, 'Nuevo')

    def test_eliminar_juego(self):
        j = Juego(nombre='Borrar', descripcion='D', precio=1.0)
        db.session.add(j)
        db.session.commit()
        db.session.delete(j)
        db.session.commit()
        self.assertEqual(Juego.query.count(), 0)

    def test_password_se_guarda_como_hash(self):
        u = User(username='charlie')
        u.set_password('secreto123')
        self.assertNotEqual(u.password_hash, 'secreto123')
        self.assertTrue(u.check_password('secreto123'))
        self.assertFalse(u.check_password('otra'))

    def test_username_es_unico(self):
        db.session.add(User(username='ana', password_hash='x'))
        db.session.commit()
        db.session.add(User(username='ana', password_hash='y'))
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()


if __name__ == '__main__':
    unittest.main()