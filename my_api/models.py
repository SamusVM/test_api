from django.db import models

from my_auth.models import User


class Post(models.Model):
    text = models.CharField(max_length=1234)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='liked by')
    created_at = models.DateTimeField(auto_now=True, verbose_name='liked at')

    class Meta:
        unique_together = ('post', 'created_by',)

    def __str__(self):
        return f"{self.post} {self.created_by} {self.created_at}"
