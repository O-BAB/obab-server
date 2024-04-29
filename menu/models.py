from django.db import models


class Type(models.Model):
    eng_name = models.CharField(max_length=50)
    kor_name = models.CharField(max_length=50)


class Fullness(models.Model):
    eng_name = models.CharField(max_length=50)
    kor_name = models.CharField(max_length=50)


class Temperature(models.Model):
    eng_name = models.CharField(max_length=50)
    kor_name = models.CharField(max_length=50)


class Spicy(models.Model):
    eng_name = models.CharField(max_length=50)
    kor_name = models.CharField(max_length=50)


class MeatType(models.Model):
    eng_name = models.CharField(max_length=50)
    kor_name = models.CharField(max_length=50)


class CookingMethod(models.Model):
    eng_name = models.CharField(max_length=50)
    kor_name = models.CharField(max_length=50)


class MenuList(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    fullness = models.ForeignKey(Fullness, on_delete=models.SET_NULL, null=True)
    temperature = models.ForeignKey(Temperature, on_delete=models.SET_NULL, null=True)
    spicy = models.ForeignKey(Spicy, on_delete=models.SET_NULL, null=True)
    meat_type = models.ForeignKey(MeatType, on_delete=models.SET_NULL, null=True)
    cooking_method = models.ForeignKey(
        CookingMethod, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name
