from django.urls import path
from . import views

urlpatterns = [
    path(
        "<str:user_id>/tweets",
        views.UserTweetViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
]
