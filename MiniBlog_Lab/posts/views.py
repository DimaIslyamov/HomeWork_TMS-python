"""Views for the posts application."""
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)

from posts.forms import PostForm
from posts.models import Post


class PostListView(ListView):
    """Display the list of posts."""

    model = Post
    context_object_name = 'posts'


class PostDetailView(DetailView):
    """Display one post."""

    model = Post
    context_object_name = 'post'


class PostCreateView(CreateView):
    """Create a new post."""

    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts:post_list')
