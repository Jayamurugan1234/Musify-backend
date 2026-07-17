from django.urls import path

from .views import (
    QueueListCreateView,
    QueueDeleteView
)

urlpatterns = [

    path(
        '',
        QueueListCreateView.as_view(),
        name='queue-list-create'
    ),

    path(
        '<int:pk>/delete/',
        QueueDeleteView.as_view(),
        name='queue-delete'
    ),
]