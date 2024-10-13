from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from .serializers import TweetSerializer
from .models import Tweet
from django.conf import settings


class Tweets(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        serializer = TweetSerializer(
            Tweet.objects.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class TweetDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound("Tweet does not exist")

    def get(self, request, pk):
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)

    def put(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.user != request.user:
            raise PermissionDenied("You can only update your own tweets")
        serializer = TweetSerializer(tweet, data=request.data, partial=True)
        if serializer.is_valid():
            tweet = serializer.save()
            serializer = TweetSerializer(tweet)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.user != request.user:
            raise PermissionDenied("You can only delete your own tweets")

        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
