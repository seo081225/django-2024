from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import User
from .serializers import UserSerializer
from tweets.models import Tweet
from tweets.serializers import TweetSerializer

@api_view(["GET"])
def user_tweets(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")

    tweets = Tweet.objects.filter(user=user)
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)
