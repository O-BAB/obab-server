# Generated by Django 5.0.3 on 2024-03-19 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_foodrecipes_thumnail_delete_foodrecipeimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodrecipes',
            name='content',
            field=models.TextField(default='content default'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='foodrecipes',
            name='thumnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumnail/'),
        ),
    ]