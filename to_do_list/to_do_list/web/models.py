from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Task(models.Model):
    TITLE_MAX_LEN = 100
    TITLE_MIN_LEN = 5

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(TITLE_MIN_LEN),
        ],
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    complete = models.BooleanField(
        default=False,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['complete']
