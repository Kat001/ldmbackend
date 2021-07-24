from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import PurchasedPackages,AllRoiIncome
from api.models import AllRoiOnRoiIncome
from Accounts.models import Account
from django.db.models import Max

class Command(BaseCommand):
    help = 'Displays current time'

    def send_roi_on_roi(self,r_obj):
        user = r_obj.user.sponsor
        if user.is_active1:
            package = PurchasedPackages.objects.filter(user=user).aggregate(Max('amount'))['amount__max']#Current Active Plan of that user
            try:
                if package >= r_obj.package_amount:
                    obj = AllRoiOnRoiIncome(user=user,from_user=r_obj.user,income=r_obj.amount)
                    user.refund += r_obj.amount
                    user.save()
                    obj.save()
            except Exception as e:
                print("error-->",e)

    def handle(self, *args, **kwargs):
        objs = PurchasedPackages.objects.all()
        for obj in objs:
            flag = False
            if obj.amount == 10:
                if obj.clickedLinks >= 2:
                    flag = True
            elif obj.amount == 50:
                if obj.clickedLinks >= 4:
                    flag = True
            elif obj.amount == 100:
                if obj.clickedLinks >= 4:
                    flag = True
            elif obj.amount == 500:
                if obj.clickedLinks >= 6:
                    flag = True
            elif obj.amount == 1000:
                if obj.clickedLinks >= 7:
                    flag = True
                
            if flag:
                if obj.days>0:
                    obj.days -= 1

                    income = 0
                    if obj.amount == 10.0:
                        income = 0.1 #1%
                    elif obj.amount == 50.0:
                        income = 1 #2%
                    elif obj.amount == 100.0:
                        income = 2 #2%
                    elif obj.amount == 500.0:
                        income = 15 #3%
                    elif obj.amount == 1000.0:
                        income = 30 #3%

                    r_obj = AllRoiIncome(user=obj.user,amount=income,package_amount=obj.amount)
                    account_obj = obj.user
                    account_obj.refund += income
                    account_obj.total_roi_income += income
                    account_obj.save()
                    r_obj.save()
                    obj.clickedLinks = 0
                    obj.save()
                    self.send_roi_on_roi(r_obj)
        print("Done!!!!!")
