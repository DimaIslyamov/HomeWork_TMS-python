"""Views for the posts application."""

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView, UpdateView, DeleteView,
)

from posts.forms import PostForm
from posts.models import Post


class PostListView(ListView):
    """Display the list of posts."""

    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return (
            Post.objects
            .filter(is_published=True)
            .select_related('author', 'category')
            .order_by('-created_at')
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Все публикации'

        return context


class PostDetailView(DetailView):
    """Display one post."""

    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return (
            Post.objects
            .filter(is_published=True)
            .select_related('author', 'category')
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post."""

    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    """Update a post."""

    model = Post
    form_class = PostForm

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    """Delete a post."""

    model = Post
    success_url = reverse_lazy('posts:post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
