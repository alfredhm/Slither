# Generated by Django 4.1.2 on 2022-10-28 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_user_pfp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.IntegerField(default=0),
        ),
    ]
