import os
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.custom_users.models import CustomUser
from apps.posts.models import Post

TEST_MEDIA = tempfile.mkdtemp()


def make_user(email):
    return CustomUser.objects.create_user(
        email=email, password='x-pass-123456', first_name='A', last_name='B',
        nationality='ES', birth_date='1990-01-01',
    )


@override_settings(MEDIA_ROOT=TEST_MEDIA)
class DeletePostTests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA, ignore_errors=True)

    def setUp(self):
        self.author = make_user('author@example.com')
        self.other = make_user('other@example.com')
        self.post = Post.objects.create(
            title='test',
            author=self.author,
            audio=SimpleUploadedFile('audio-1.mp3', b'fake mp3', content_type='audio/mpeg'),
        )
        self.audio_path = self.post.audio.path

    def auth(self, user):
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_author_delete_removes_post_and_file(self):
        self.auth(self.author)
        self.assertTrue(os.path.exists(self.audio_path))

        response = self.client.delete(f'/v1/posts/delete/{self.post.id}')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
        self.assertFalse(os.path.exists(self.audio_path))

    def test_other_user_gets_403_and_nothing_is_deleted(self):
        self.auth(self.other)

        response = self.client.delete(f'/v1/posts/delete/{self.post.id}')

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())
        self.assertTrue(os.path.exists(self.audio_path))

    def test_anonymous_cannot_delete(self):
        response = self.client.delete(f'/v1/posts/delete/{self.post.id}')

        self.assertEqual(response.status_code, 401)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())
