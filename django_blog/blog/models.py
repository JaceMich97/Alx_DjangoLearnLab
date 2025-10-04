from django.db import models
from django.contrib.auth import get_user_model

class Post(models.Model):
    """
    A simple blog post.
    - title: short post title
    - content: the main body
    - published_date: set automatically when created
    - author: FK to the user who wrote the post
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        return self.title
