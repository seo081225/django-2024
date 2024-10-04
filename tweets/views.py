from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from .models import Tweet
from .serializers import TweetSerializer


class TweetViewSet(ModelViewSet):

    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()