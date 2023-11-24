from django.db import models

from django.utils.translation import gettext_lazy as _
from core.functions import upload_food_img

from accounts.models import User


class Food(models.Model):
    TYPE_CHOICES = (
        ("noodle", "면"),
        ("rice", "밥"),
        ("bread", "빵"),
        ("meat", "육류"),
        ("SOUP", "국물"),
        ("DESSERT", "디저트"),
    )
    WEIGHT_CHOICES = (("heavy", "무거움"), ("light", "가벼움"))
    TEMPERATURE_CHOICES = (("hot", "뜨거움"), ("warm", "따뜻함"), ("cool", "차거움"))
    SPICY_CHOICES = (
        ("very_spicy", "매우 매움"),
        ("spicy", "매운맛"),
        ("normal", "보통"),
        ("little_spicy", "덜 매운 맛"),
        ("mild", "순함"),
    )
    MEAT_CHOICES = (
        ("beef", "소 고기"),
        ("pork", "돼지 고기"),
        ("chicken", "닭 고기"),
        ("vegan", "비건"),
        ("meatless", "고기 없음"),
    )
    METHOD_CHOICES = (
        ("grilled", "구움"),
        ("fried", "튀김"),
        ("steamed", "찜"),
        ("boiled", "끓임"),
        ("raw", "날것"),
    )

    name = models.CharField(max_length=30)
    image = models.ImageField(
        _("food image"),
        upload_to=upload_food_img,
        default="img/default/default_food_img.jpg",
    )
    food_type = models.CharField(_("음식 종류"), max_length=20, choices=TYPE_CHOICES)
    weight = models.CharField(_("무게"), max_length=10, choices=WEIGHT_CHOICES)
    temperature = models.CharField(_("온도"), max_length=10, choices=TEMPERATURE_CHOICES)
    spicy_level = models.CharField(_("매운 정도"), max_length=15, choices=SPICY_CHOICES)
    meat_type = models.CharField(_("고기 종류"), max_length=15, choices=MEAT_CHOICES)
    cooking_method = models.CharField(_("조리 방식"), max_length=10, choices=METHOD_CHOICES)

    suggestion_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_activate = models.BooleanField(default=False)

    def __str__(self):
        return self.name
