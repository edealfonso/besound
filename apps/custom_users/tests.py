from rest_framework.test import APITestCase

from apps.custom_users.models import CustomUser


class RegisterTests(APITestCase):
    def payload(self, **overrides):
        data = {
            'email': 'ana@example.com',
            'first_name': 'Ana',
            'last_name': 'García',
            'nationality': 'ES',
            'birth_date': '1990-01-01',
            'password': 'un-sonido-largo-42',
        }
        data.update(overrides)
        return data

    def test_register_does_not_return_password(self):
        response = self.client.post('/v1/register', self.payload(), format='json')

        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.data)

    def test_register_stores_usable_hashed_password(self):
        self.client.post('/v1/register', self.payload(), format='json')

        user = CustomUser.objects.get(email='ana@example.com')
        self.assertNotEqual(user.password, 'un-sonido-largo-42')
        self.assertTrue(user.check_password('un-sonido-largo-42'))

    def test_register_rejects_weak_password(self):
        response = self.client.post('/v1/register', self.payload(password='123'), format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(CustomUser.objects.exists())

    def test_registered_user_can_log_in(self):
        self.client.post('/v1/register', self.payload(), format='json')

        response = self.client.post(
            '/v1/login', {'username': 'ana@example.com', 'password': 'un-sonido-largo-42'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
