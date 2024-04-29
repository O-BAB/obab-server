import os

from django.utils import timezone


def upload_user_directory(instance, filename):
    email = instance.email
    now = timezone.now()

    # img/profile/year/month/user_user.id_20230405_name_123128_.png
    return "img/profile/{year}/{month}/user_{user_id}_{now}_{name}_{microsecond}_{extension}".format(
        year=now.year,
        month=now.month,
        user_id=instance.id,
        now=now.strftime("%Y%m%d"),
        name=email.split("@")[0],
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )


def upload_thumnail_directory(instance, filename):
    category = instance.categoryCD
    email = instance.user.email
    now = timezone.now()

    # img/category/year/month/day/user_user.id/thumnail_20230405_s94203_123128.png
    return "img/{category}/{year}/{month}/{day}/user_{user_id}/thumnail_{now}_{name}_{microsecond}_{extension}".format(
        category=category,
        year=now.year,
        month=now.month,
        day=now.day,
        user_id=instance.user.id,
        now=now.strftime("%Y%m%d"),
        name=email.split("@")[0],
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )


def upload_post_image_directory(instance, filename):
    img_id = instance.id
    category = instance.foodrecipe.categoryCD
    email = instance.foodrecipe.user.email
    now = timezone.now()

    # img/category/year/month/day/user_user.id/content_img/instance.id_20230405_s94203_123128.png
    return "img/{category}/{year}/{month}/{day}/user_{user_id}/content_img/{img_id}_{now}_{name}_{microsecond}_{extension}".format(
        category=category,
        year=now.year,
        month=now.month,
        day=now.day,
        user_id=instance.foodrecipe.user.id,
        img_id=img_id,
        now=now.strftime("%Y%m%d"),
        name=email.split("@")[0],
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )
