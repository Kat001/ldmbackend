from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from Accounts.models import Account
from .models import Fund, LevelIncome, PurchasedPackages
from .serializers import UserSerializer

# Create your views here.


class PurchasePackage(APIView):
    def defineDays(self, amount):
        if amount == 50:
            return 67
        elif amount == 100:
            return 67
        elif amount == 500:
            return 50
        elif amount == 1000:
            return 50
        elif amount == 5000:
            return 40
        elif amount == 10000:
            return 40

    def post(self, request, format=None):
        user = Account.objects.get(username="admin")  # request.user
        amount = 50
        try:
            fund_obj = Fund.objects.get(user=user)
            if(fund_obj.available_fund >= amount):
                fund_obj.available_fund -= int(amount)
                days = self.defineDays(int(amount))
                package = PurchasedPackages(
                    user=user, amount=int(amount), days=days)
                user.is_active1 = True

                # Assign Level Income................

                i = 5
                obj = user
                while obj.sponsor != None and i != 0:
                    obj = obj.sponsor
                    if obj.is_active1:
                        if i == 5:
                            income = (int(amount)*10/100)
                            obj.total_level_income += income
                            obj.refund += income
                            levelIncome_obj = LevelIncome(
                                user=obj, level='1', amount=income, activated_user=user)
                            levelIncome_obj.save()
                        if i == 4:
                            income = (int(amount)*2/100)
                            obj.total_level_income += income
                            obj.refund += income
                            levelIncome_obj = LevelIncome(
                                user=obj, level='2', amount=income, activated_user=user)
                            levelIncome_obj.save()
                        if i == 3:
                            income = (int(amount)*1/100)
                            obj.total_level_income += income
                            obj.refund += income
                            levelIncome_obj = LevelIncome(
                                user=obj, level='3', amount=income, activated_user=user)
                            levelIncome_obj.save()
                        if i == 2:
                            income = (int(amount)*1/100)
                            obj.total_level_income += income
                            obj.refund += income
                            levelIncome_obj = LevelIncome(
                                user=obj, level='4', amount=income, activated_user=user)
                            levelIncome_obj.save()

                        if i == 1:
                            income = (int(amount)*1/100)
                            obj.total_level_income += income
                            obj.refund += income
                            levelIncome_obj = LevelIncome(
                                user=obj, level='5', amount=income, activated_user=user)
                            levelIncome_obj.save()

                        i = i - 1
                        obj.save()
                    else:
                        i = i - 1
                user.save()
                package.save()
                fund_obj.save()

                return Response({"message": "Package purchased seccessfully!"})

            else:
                return Response({'message': "Not enough balance"})

        except Exception as e:
            print(str(e))

        # serializer = UserSerializer(directUsers, many=True)
        return Response({"message": "hghgs"})


class LevelOne(APIView):
    def get(self, request, format=None):
        user = Account.objects.get(username="admin")  # request.user
        directUsers = Account.objects.filter(sponsor=user)

        serializer = UserSerializer(directUsers, many=True)
        return Response(serializer.data)


class LevelTwo(APIView):
    def get(self, request, format=None):
        user = Account.objects.get(username="admin")  # request.user
        l = []

        objs1 = Account.objects.filter(sponsor=user)

        for o in objs1:
            obj2 = Account.objects.filter(sponsor=o)
            for i in obj2:
                l.append(i.id)

        objs = Account.objects.filter(id__in=l)
        serializer = UserSerializer(objs, many=True)

        return Response(serializer.data)


class LevelThree(APIView):
    def get(self, request, format=None):
        user = Account.objects.get(username="admin")  # request.user
        l = []

        objs1 = Account.objects.filter(sponsor=user)

        for o in objs1:
            obj2 = Account.objects.filter(sponsor=o)
            for o2 in obj2:
                obj3 = Account.objects.filter(sponsor=o2)
                for i in obj3:
                    l.append(i.id)
        objs = Account.objects.filter(id__in=l)
        serializer = UserSerializer(objs, many=True)
        return Response(serializer.data)


class LevelFour(APIView):
    def get(self, request, format=None):
        user = Account.objects.get(username="admin")  # request.user
        l = []

        objs1 = Account.objects.filter(sponsor=user)

        for o in objs1:
            obj2 = Account.objects.filter(sponsor=o)
            for o2 in obj2:
                obj3 = Account.objects.filter(sponsor=o2)
                for o3 in obj3:
                    obj4 = Account.objects.filter(sponsor=o3)
                    for i in obj4:
                        l.append(i.id)

        objs = Account.objects.filter(id__in=l)

        serializer = UserSerializer(objs, many=True)
        return Response(serializer.data)


class LevelFive(APIView):
    def get(self, request, format=None):
        user = Account.objects.get(username="admin")  # request.user
        l = []

        objs1 = Account.objects.filter(sponsor=user)

        for o in objs1:
            obj2 = Account.objects.filter(sponsor=o)
            for o2 in obj2:
                obj3 = Account.objects.filter(sponsor=o2)
                for o3 in obj3:
                    obj4 = Account.objects.filter(sponsor=o3)
                    for o4 in obj4:
                        obj5 = Account.objects.filter(sponsor=o4)
                        for i in obj5:
                            l.append(i.id)

        objs = Account.objects.filter(id__in=l)
        serializer = UserSerializer(objs, many=True)
        return Response(serializer.data)
