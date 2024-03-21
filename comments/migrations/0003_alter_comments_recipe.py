# Generated by Django 5.0.3 on 2024-03-20 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comments_created_at_comments_updated_at'),
        ('recipes', '0010_remove_foodrecipes_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.foodrecipes'),
        ),
    ]
