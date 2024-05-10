import os
import uuid
from django.utils import timezone


def upload_user_directory(instance, filename):
    email = instance.email
    now = timezone.now()

    base_name = email.split("@")[0]
    file_extension = os.path.splitext(filename)[1]
    unique_id = uuid.uuid4()

    # 경로를 안전하게 연결
    path = os.path.join(
        "img",
        str(now.year),
        str(now.month),
        str(now.day),
        f"user_{instance.id}",
        f'{now.strftime("%Y%m%d")}_{base_name}_{unique_id}{file_extension}',
    )
    return path


def upload_image_directory(instance, filename):
    email = instance.user.email
    now = timezone.now()

    base_name = email.split("@")[0]
    file_extension = os.path.splitext(filename)[1]
    unique_id = uuid.uuid4()

    # 경로를 안전하게 연결
    path = os.path.join(
        "img",
        str(now.year),
        str(now.month),
        str(now.day),
        f"user_{instance.user.id}",
        f'{now.strftime("%Y%m%d")}_{base_name}_{unique_id}{file_extension}',
    )
    return path


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
