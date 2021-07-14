from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from Accounts.models import Account
from .models import Fund, LevelIncome, PurchasedPackages,AllRoiIncome,AllRoiOnRoiIncome
from .serializers import UserSerializer, PackageSerializer,RoiSerializer,LevelIncomeSerializer,RoiOnRoiIncomeSerializer,RegisterSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework import generics, permissions
from django.contrib.auth.hashers import check_password



# Create your views here.

class LevelIncome1(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        
        leveincome = LevelIncome.objects.filter(user = user)
        serializer = LevelIncomeSerializer(leveincome, many=True)

        return Response({"data":serializer.data}, status=200)


class UserProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        fund_obj = Fund.objects.get(user=user)

        if user.sponsor is None:
            sponsor = "admin"
        else:
            sponsor = str(user.sponsor.username)

        return Response({'name': str(user.first_name) + " " + str(user.last_name),
                          'fund':fund_obj.available_fund,
                          'phone' : user.phon_no,
                          'username':user.username,
                          'first_name':str(user.first_name),
                          'last_name':str(user.last_name),
                          'email':str(user.email),
                          'address':str(user.address),
                          'sponsor': sponsor,
                          'registration':str(user.date_joined)
        }, status=200)

class TransferFund(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        trans_user = str(request.data['username'])
        amount = float(request.data['fund'])

        try:
            trans_obj = Account.objects.get(username=trans_user)
            fund_obj_trans = Fund.objects.get(user = trans_obj)
            fund_obj_user = Fund.objects.get(user=user)
            if(float(fund_obj_user.available_fund >= amount)):
                fund_obj_user.available_fund -= amount
                fund_obj_trans.available_fund += amount
                fund_obj_user.save()
                fund_obj_trans.save()
                return Response({'message': "success"}, status=200)

            else:
                return Response({'message': "You do not have enough balance to send!!"}, status=201)

        except Exception as e:
            print("ijiosd----->",e)
            return Response({'message': str(e)}, status=404)
        
 

        return Response({'data': serializer.data}, status=200)





class MainPage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        profit = user.total_level_income + user.total_roi_income + 7

        return Response({'total_income': user.refund,
                          'total_withdrawal':user.total_withdrawal,
                          'total_profit' : profit,
        }, status=200)


class CheckDailyIncome(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        amount = float(request.data['amount'])
        print(amount)
        roi_income = AllRoiIncome.objects.filter(user=user,package_amount = amount)
        serializer = RoiSerializer(roi_income, many=True)

        return Response({'data': serializer.data}, status=200)




class UserDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        packages = PurchasedPackages.objects.filter(user=user)
        serializer = PackageSerializer(packages, many=True)

        return Response({'data': serializer.data}, status=200)

class RoiOnRoi(APIView):

    def get(self, request, format=None):
        user = request.user
        roi = AllRoiOnRoiIncome.objects.filter(user=user)
        serializer = RoiOnRoiIncomeSerializer(roi, many=True)

        return Response({'data': serializer.data}, status=200)


class ReturnPack(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        packages = PurchasedPackages.objects.filter(user=user)
        serializer = PackageSerializer(packages, many=True)

        return Response({'data': serializer.data}, status=200)


class PurchasePackage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def defineDays(self, amount):
        if amount == 10:
            return 200
        elif amount == 50:
            return 125
        elif amount == 100:
            return 125
        elif amount == 500:
            return 100
        elif amount == 1000:
            return 100

    def post(self, request, format=None):
        user = request.user
        amount = request.data['amount']

        # Check That package is already purchased........
        try:
            package = PurchasedPackages.objects.get(user=user,amount=int(amount))
            return Response({'message': "This Package is already Purchased!!"}, status=404)
        except Exception as e:
            pass
  
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
                            income = (int(amount)*5/100)
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

                return Response({"message": "Package purchased seccessfully!"}, status=200)

            else:
                return Response({'message': "Not enough balance"}, status=404)

        except Exception as e:
            print(str(e))

        # serializer = UserSerializer(directUsers, many=True)
        return Response({"message": "Contact to admin"}, status=404)


class LevelOne(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        directUsers = Account.objects.filter(sponsor=user)

        serializer = UserSerializer(directUsers, many=True)
        return Response({"data": serializer.data})


class LevelTwo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        l = []

        objs1 = Account.objects.filter(sponsor=user)

        for o in objs1:
            obj2 = Account.objects.filter(sponsor=o)
            for i in obj2:
                l.append(i.id)

        objs = Account.objects.filter(id__in=l)
        serializer = UserSerializer(objs, many=True)

        return Response({"data": serializer.data})


class LevelThree(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
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
        return Response({"data": serializer.data})


class LevelFour(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
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
        return Response({"data": serializer.data})


class LevelFive(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
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
        return Response({"data": serializer.data})


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Sending the email........(mailgun is not free so i do not have credentials)
        # msg = "Your Account has been created successfully!"
        # send_mail('account', msg, 'noreply@bottlenose.co', ['vitor@freitas.com'])
        #
        # print("message send successfully!!")
        if user == 'error':
            return Response({'message':"error"},status=404)


        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        },status=200)

class ChangePassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        currentPassword = str(request.data['cPassword'])
        newPassword = str(request.data['nPassword'])

        #check password...
        isPass = user.check_password(currentPassword)
        print(isPass)
        
        if isPass:
            user.set_password(newPassword)
            user.save()
            return Response({'data':"Password Changed successfully!!"},status=200)

        else:
            return Response({'data':"Old password is not correct!!"},status=404)

