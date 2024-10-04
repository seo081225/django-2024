from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import User
from .serializers import UserSerializer

from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

class UserTweetViewSet(ModelViewSet):
    serializer_class = TweetSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')

        try:
            int(user_id) 
        except ValueError:
            raise ValidationError(detail="User ID must be an integer.", code=400)

        if not User.objects.filter(id=user_id).exists():
            raise NotFound(detail="User not found with the given ID.", code=404)

        return Tweet.objects.filter(user__id=user_id)
