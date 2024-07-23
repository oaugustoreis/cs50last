from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=140)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"Post {self.id}, by {self.author} on {self.date.strftime('%d -%b -%Y %H:%M')}"
    
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    def __str__(self) :
        return f"{self.user} is following by {self.user_follow} "