# Generated by Django 3.0.6 on 2020-11-14 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='user_id',
            field=models.IntegerField(unique=True, verbose_name='User Id'),
        ),
    ]
