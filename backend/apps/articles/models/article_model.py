from django.db import models

from django.conf import settings


class Article(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


    
    # Зовнішні модулі
    # tags
    # like
    # comment
    # file
    # скарги
