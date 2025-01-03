from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse


user = get_user_model()


class Core(models.Model):
    title = models.CharField(
        max_length=200,
    )

    excerpt = models.TextField(
        null=True,
        blank=True,
    )

    author = models.ForeignKey(
        to=user,
        on_delete=models.CASCADE,
        related_name='core',
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
    )

    published = models.DateTimeField(
        default=timezone.now,
    )

    def get_absolute_url(self):
        return reverse('core:single', args=[self.slug])

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title
