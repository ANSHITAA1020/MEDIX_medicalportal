from django.db import models


class Article(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()
    urlToImage = models.URLField(null=True, blank=True)
    publishedAt = models.DateTimeField()
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title