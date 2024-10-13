from rest_framework import serializers
from .models import Tweet
from users.models import User


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    like_count = serializers.IntegerField(source='total_likes_count', read_only=True)

    class Meta:
        model = Tweet
        fields = ["pk", "payload", "user", "like_count", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["pk", "username", "password", "name", "avatar", "gender"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user