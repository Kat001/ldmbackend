from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import PurchasedPackages,AllRoiIncome
from Accounts.models import Account

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        objs = PurchasedPackages.objects.all()
        for obj in objs:
            if obj.days>0:
                obj.days -= 1

                income = 0
                if obj.amount == 50.0:
                    income = 1.5 #3%
                elif obj.amount == 100.0:
                    income = 3 #3%
                elif obj.amount == 500.0:
                    income = 20 #4%
                elif obj.amount == 1000.0:
                    income = 40 #4%
                elif obj.amount == 5000.0:
                    income = 250 #5%
                elif obj.amount == 10000.0:
                    income = 500 #5%

                r_obj = AllRoiIncome(user=obj.user,amount=income,package_amount=obj.amount)
                account_obj = obj.user
                account_obj.refund += income
                account_obj.total_roi_income += income
                account_obj.save()
                r_obj.save()
                obj.save()
        print("Done!!!!!")
