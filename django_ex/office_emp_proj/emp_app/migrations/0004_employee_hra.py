# Generated by Django 3.0.14 on 2023-02-01 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp_app', '0003_userprofileinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='hra',
            field=models.IntegerField(default=0),
        ),
    ]