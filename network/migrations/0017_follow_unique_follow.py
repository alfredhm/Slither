# Generated by Django 4.1.2 on 2022-10-30 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_remove_user_pfp_alter_follow_following_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('followed_user', 'following_user'), name='unique_follow'),
        ),
    ]
