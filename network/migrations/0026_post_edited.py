# Generated by Django 4.1.4 on 2023-04-27 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0025_alter_user_pfp'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
