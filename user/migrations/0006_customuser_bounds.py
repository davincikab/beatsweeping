# Generated by Django 3.0.6 on 2020-11-04 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20201104_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bounds',
            field=models.CharField(default='[-117.13265508413315, 32.755312373407506, -117.12893486022949, 32.75729060724447]', max_length=50, verbose_name='Bounds'),
            preserve_default=False,
        ),
    ]