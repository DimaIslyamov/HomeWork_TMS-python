from django.urls import path

from events import views

app_name = 'events'
urlpatterns = [
    path(
        "",
        views.EventListView.as_view(),
        name="event_list",
    ),
    path(
        "create/",
        views.EventCreateView.as_view(),
        name="event_create",
    ),
    path(
        "my-events/",
        views.MyEventListView.as_view(),
        name="my_event_list",
    ),
    path(
        "my-registrations/",
        views.MyRegistrationListView.as_view(),
        name="my_registration_list",
    ),

    path(
        "<int:pk>/update/",
        views.EventUpdateView.as_view(),
        name="event_update",
    ),
    path(
        "<int:pk>/delete/",
        views.EventDeleteView.as_view(),
        name="event_delete",
    ),
    path(
        "<int:pk>/join/",
        views.join_event,
        name="event_join",
    ),
    path(
        "<int:pk>/leave/",
        views.leave_event,
        name="event_leave",
    ),
    path(
        "category/<int:category_id>/",
        views.EventListView.as_view(),
        name="events_by_category",
    ),

    path(
        "<slug:slug>/",
        views.EventDetailView.as_view(),
        name="event_detail",
    ),
]
