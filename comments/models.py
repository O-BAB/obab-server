from django.db import models
from accounts.models import User
from recipes.models import FoodRecipes
from core.models import TimeStampedModel


class Comments(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(FoodRecipes, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    root = models.ForeignKey(
        "self",
        related_name="root_comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "{} : {}".format(self.user, self.text)
