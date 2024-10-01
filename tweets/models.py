from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Tweet(BaseModel):
    payload = models.TextField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tweet(payload={self.payload} / like_count={self.likes.count()} / author={self.user.pk};{self.user.username})"
    
    def total_likes_count(self):
        return self.likes.count()
    
class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user.username} liked '{self.tweet.payload}'"