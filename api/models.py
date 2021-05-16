from django.db import models
from Accounts.models import Account

# Create your models here.


class Fund(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    available_fund = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class DirectIncome(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    activated_user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="activated_id")
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


class LevelIncome(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    activated_user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="activated_iid")
    date = models.DateField(auto_now_add=True)
    level = models.CharField(max_length=10, default="")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class FundTransferHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    transfer_user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="TranferUser")
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)

    def __str__(self):
        return(f'{self.user.username}')


class PurchasedPackages(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    is_withdrawal = models.BooleanField(default=False)
    days = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class AllRoiIncome(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    package_amount = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


class AllRoiOnRoiIncome(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="FromUser")
    amount = models.FloatField(default=0)
    income = models.FloatField(default=0)
    level = models.CharField(max_length=5, default="")

    def __str__(self):
        return self.user.username


class Bank_Info(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=40, default="-")
    account_number = models.CharField(max_length=30, default='-')
    branch_name = models.CharField(max_length=40, default='-')
    ifsc_code = models.CharField(max_length=20, default="-")
    bank_name = models.CharField(max_length=30, default='-')
    nominee_name = models.CharField(max_length=30, default="-")
    aadhar_number = models.CharField(max_length=12, default="-")
    pan_number = models.CharField(max_length=10, default="-")
    aadhar_image = models.ImageField(
        default="default.jpg", upload_to="adhar_pics", null=True, blank=True)
    pan_image = models.ImageField(
        default="default.jpg", upload_to="pan_pics", null=True, blank=True)
    p_image = models.ImageField(
        default="default.jpg", upload_to="profile_pics")
    cheak = models.BooleanField(default=False)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return(f'{self.user.username}')


class book(models.Model):
    name = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=300, default="")
    trailer = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.name
