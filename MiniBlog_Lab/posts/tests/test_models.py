from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post


class PostModelTests(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

        self.post = Post.objects.create(
            author=self.user,
            title="Test post",
            content="Test content",
            is_published=True,
        )

    def test_get_absolute_url_uses_slug(self):
        self.assertEqual(
            self.post.get_absolute_url(),
            f"/posts/{self.post.slug}/",
        )