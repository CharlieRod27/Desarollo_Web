import unittest
from app import create_app
from models import db, Juego


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        j = Juego(nombre='X', descripcion='Y', precio=1.23)
        db.session.add(j)
        db.session.commit()
        self.juego_id = j.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def valido(self, **extra):
        datos = {'nombre': 'Nuevo', 'descripcion': 'Desc', 'precio': 10}
        datos.update(extra)
        return datos

    def test_get_lista_200(self):
        resp = self.client.get('/api/juegos')
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.get_json(), list)

    def test_get_lista_contenido(self):
        data = self.client.get('/api/juegos').get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], 'X')

    def test_get_juego_por_id_200(self):
        resp = self.client.get(f'/api/juegos/{self.juego_id}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['descripcion'], 'Y')

    def test_get_juego_inexistente_404(self):
        self.assertEqual(self.client.get('/api/juegos/9999').status_code, 404)

    def test_post_crea_juego_201(self):
        resp = self.client.post('/api/juegos', json=self.valido())
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.get_json()['nombre'], 'Nuevo')
        self.assertEqual(Juego.query.count(), 2)

    def test_post_campos_faltantes_400(self):
        resp = self.client.post('/api/juegos', json={'nombre': 'Solo nombre'})
        self.assertEqual(resp.status_code, 400)

    def test_post_precio_invalido_400(self):
        resp = self.client.post('/api/juegos', json=self.valido(precio='gratis'))
        self.assertEqual(resp.status_code, 400)

    def test_post_cuerpo_no_json_400(self):
        resp = self.client.post('/api/juegos', data='esto no es json',
                                content_type='text/plain')
        self.assertEqual(resp.status_code, 400)

    def test_put_actualiza_200(self):
        resp = self.client.put(f'/api/juegos/{self.juego_id}',
                               json=self.valido(nombre='Editado', precio=999))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['nombre'], 'Editado')
        self.assertEqual(db.session.get(Juego, self.juego_id).precio, 999.0)

    def test_put_inexistente_404(self):
        resp = self.client.put('/api/juegos/9999', json=self.valido())
        self.assertEqual(resp.status_code, 404)

    def test_delete_204(self):
        resp = self.client.delete(f'/api/juegos/{self.juego_id}')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Juego.query.count(), 0)

    def test_delete_inexistente_404(self):
        self.assertEqual(self.client.delete('/api/juegos/9999').status_code, 404)


if __name__ == '__main__':
    unittest.main()