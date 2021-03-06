# Generated by Django 3.1 on 2021-05-14 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('thumbnail', models.CharField(default='', max_length=300)),
                ('trailer', models.CharField(default='', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedPackages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
                ('percent10', models.FloatField(default=0)),
                ('total_income', models.FloatField(default=0)),
                ('day1', models.BooleanField(default=True)),
                ('is_withdrawal', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LevelIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('level', models.CharField(default='', max_length=10)),
                ('amount', models.IntegerField(default=0)),
                ('activated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activated_iid', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FundTransferHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField(default=0)),
                ('transfer_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TranferUser', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_fund', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DirectIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.FloatField(default=0)),
                ('activated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activated_id', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bank_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_name', models.CharField(default='-', max_length=40)),
                ('account_number', models.CharField(default='-', max_length=30)),
                ('branch_name', models.CharField(default='-', max_length=40)),
                ('ifsc_code', models.CharField(default='-', max_length=20)),
                ('bank_name', models.CharField(default='-', max_length=30)),
                ('nominee_name', models.CharField(default='-', max_length=30)),
                ('aadhar_number', models.CharField(default='-', max_length=12)),
                ('pan_number', models.CharField(default='-', max_length=10)),
                ('aadhar_image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='adhar_pics')),
                ('pan_image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='pan_pics')),
                ('p_image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('cheak', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AllRoiOnRoiIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField(default=0)),
                ('income', models.FloatField(default=0)),
                ('level', models.CharField(default='', max_length=5)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FromUser', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AllRoiIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField(default=0)),
                ('package_amount', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
