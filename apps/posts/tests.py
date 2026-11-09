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


# Real file headers, as recorded by browsers (Chrome/Firefox: WebM, Safari: MP4)
WEBM = b'\x1a\x45\xdf\xa3' + b'\x00' * 60
MP3 = b'ID3\x04' + b'\x00' * 60
MP4 = b'\x00\x00\x00\x20ftypM4A ' + b'\x00' * 60


@override_settings(MEDIA_ROOT=TEST_MEDIA, MAX_AUDIO_UPLOAD_MB=1)
class CreatePostTests(APITestCase):
    def setUp(self):
        user = make_user('author@example.com')
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def upload(self, content, name='audio-1.mp3', content_type='audio/mp3'):
        audio = SimpleUploadedFile(name, content, content_type=content_type)
        return self.client.post('/v1/posts/new', {'title': 'hola', 'audio': audio}, format='multipart')

    def test_accepts_webm_named_mp3_as_the_frontend_sends_it(self):
        response = self.upload(WEBM)
        self.assertEqual(response.status_code, 201, response.data)

    def test_accepts_real_mp3_and_safari_mp4(self):
        self.assertEqual(self.upload(MP3).status_code, 201)
        self.assertEqual(self.upload(MP4, name='audio-2.m4a', content_type='audio/mp4').status_code, 201)

    def test_rejects_non_audio_content_even_with_mp3_name(self):
        response = self.upload(b'<html><script>alert(1)</script></html>')
        self.assertEqual(response.status_code, 400)
        self.assertIn('audio', response.data)
        self.assertFalse(Post.objects.exists())

    def test_rejects_files_over_the_size_limit(self):
        response = self.upload(WEBM + b'\x00' * (1024 * 1024))
        self.assertEqual(response.status_code, 400)
        self.assertIn('audio', response.data)


class ListPostsTests(APITestCase):
    def setUp(self):
        user = make_user('author@example.com')
        for i in range(5):
            Post.objects.create(title=f'post {i}', author=user, audio=f'audio/{i}.mp3')

    def test_without_params_returns_plain_list_like_before(self):
        response = self.client.get('/v1/posts/list')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 5)

    def test_limit_and_offset_paginate(self):
        response = self.client.get('/v1/posts/list?limit=2&offset=2')
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])

    def test_limit_is_capped(self):
        response = self.client.get('/v1/posts/list?limit=1000')
        self.assertEqual(response.data['count'], 5)
