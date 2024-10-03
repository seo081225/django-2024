from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Tweet, User
from .serializers import TweetSerializer

# 1. 모든 Tweets 리스트
@api_view(["GET"])
def tweets_list(request):
    tweets = Tweet.objects.all()
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)

# 2. 특정 User의 Tweets 리스트
@api_view(["GET"])
def user_tweets(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")

    tweets = Tweet.objects.filter(user=user)
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)
