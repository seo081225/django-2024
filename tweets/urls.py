from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.TweetViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
]