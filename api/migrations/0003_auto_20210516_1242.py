# Generated by Django 2.2.14 on 2021-05-16 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210514_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasedpackages',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
