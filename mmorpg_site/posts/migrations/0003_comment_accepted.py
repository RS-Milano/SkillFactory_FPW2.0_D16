# Generated by Django 3.2.7 on 2021-09-05 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_rename_post_category_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
