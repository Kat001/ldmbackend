from api.models import PurchasedPackages,AllRoiIncome,LevelIncome,AllRoiOnRoiIncome,Links
from Accounts.models import Account
from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password,check_password
import random
from api.models import Fund

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("username", "first_name", "last_name",)


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedPackages
        fields = '__all__'

class RoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllRoiIncome
        fields = '__all__'

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = '__all__'

class LevelIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelIncome
        fields = '__all__'

class RoiOnRoiIncomeSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    class Meta:
        model = AllRoiOnRoiIncome
        fields = ('date', 'income', 'user', 'from_user')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    spn = serializers.CharField(required=True)
    class Meta:
        model = Account
        fields = ('id','spn','first_name','last_name','email', 'phon_no','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            print(validated_data['spn'])
            pass12 = make_password(validated_data['password'])
            sponsor = Account.objects.get(username=validated_data['spn'])
            while True:
                rand_num = random.randint(500000,599999)
                u_name = 'CC' + str(rand_num)
                if Account.objects.filter(username=u_name).exists():
                    pass
                else:
                    break
            user = Account(username = u_name,sponsor=sponsor,first_name=validated_data['first_name'], 
                            last_name=validated_data['last_name'],email=validated_data['email'],
                            phon_no=validated_data['phon_no'],password=pass12,refund=0.5)
            user.save() 
            fund = Fund(user = user)
            fund.save()
            return user
        except Exception as e:
            print("datad is is-->",e)
            return "error"

        
        
