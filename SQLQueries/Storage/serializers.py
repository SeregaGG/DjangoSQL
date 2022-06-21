from rest_framework import serializers
from .models import Store, Purchase


class StoreSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Store(**self.validated_data)

    class Meta:
        model = Store
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Purchase(**self.validated_data)

    class Meta:
        model = Purchase
        fields = '__all__'