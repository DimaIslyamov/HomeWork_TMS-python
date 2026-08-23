from django.urls import path

from events import views


app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('about/', views.event_about, name='event_about'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
]
