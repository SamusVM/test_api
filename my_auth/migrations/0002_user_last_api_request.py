# Generated by Django 4.0.6 on 2022-07-28 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_api_request',
            field=models.DateTimeField(null=True),
        ),
    ]