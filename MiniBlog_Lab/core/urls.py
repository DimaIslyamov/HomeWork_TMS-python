from django.urls import path
from django.views.generic import RedirectView

from core import views


app_name = 'core'

urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="posts:post_list", permanent=False),
        name="home",
    ),
    path("request-demo/", views.request_demo, name="request_demo"),
]
