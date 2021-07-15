# Generated by Django 3.1 on 2021-07-14 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_links_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='user',
        ),
        migrations.AddField(
            model_name='tasks',
            name='package',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='api.purchasedpackages'),
            preserve_default=False,
        ),
    ]