# Generated by Django 3.1 on 2021-07-13 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210703_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allroiincome',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='allroionroiincome',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]