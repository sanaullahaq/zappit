from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # this is to show the post in descending order in django admin panel
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


# to prevent a user from voting a post twice ,that's why we made a Vote model separately
class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
