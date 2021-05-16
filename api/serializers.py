from api.models import PurchasedPackages
from Accounts.models import Account
from rest_framework import fields, serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("username", "first_name", "last_name",)


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedPackages
        fields = '__all__'
