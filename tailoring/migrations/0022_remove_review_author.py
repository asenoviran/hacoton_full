# Generated by Django 4.2 on 2023-04-28 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0021_alter_orderstatus_options_review_like_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
    ]
