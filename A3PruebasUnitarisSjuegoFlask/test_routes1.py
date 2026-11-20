import unittest
from app import create_app
from models import db, User


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def crear_usuario(self, username='charlie', password='1234'):
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()

    def login(self, username='charlie', password='1234'):
        return self.client.post('/auth/login',
                                data={'username': username, 'password': password})

    def test_inicio_redirige_a_juegos(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers['Location'].endswith('/juegos'))

    def test_juegos_requiere_login(self):
        resp = self.client.get('/juegos')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/auth/login', resp.headers['Location'])

    def test_login_incorrecto_no_entra(self):
        self.crear_usuario()
        resp = self.login(password='mal')
        self.assertEqual(resp.status_code, 200)            # vuelve a mostrar el formulario
        self.assertIn('incorrectos', resp.get_data(as_text=True))
        self.assertEqual(self.client.get('/juegos').status_code, 302)

    def test_login_correcto_permite_ver_juegos(self):
        self.crear_usuario()
        resp = self.login()
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get('/juegos')
        self.assertEqual(resp.status_code, 200)

    def test_logout_cierra_sesion(self):
        self.crear_usuario()
        self.login()
        resp = self.client.get('/auth/logout')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.client.get('/juegos').status_code, 302)

    def test_registro_crea_usuario(self):
        resp = self.client.post('/auth/register',
                                data={'username': 'nuevo', 'password': 'abcdef',
                                      'password2': 'abcdef'})
        self.assertEqual(resp.status_code, 302)
        self.assertIsNotNone(User.query.filter_by(username='nuevo').first())

    def test_ruta_inexistente_404(self):
        self.assertEqual(self.client.get('/no-existe').status_code, 404)


if __name__ == '__main__':
    unittest.main()