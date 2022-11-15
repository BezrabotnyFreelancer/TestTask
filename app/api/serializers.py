from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault
from datetime import datetime
from main.models import Profile, Category, Transaction


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'balance', 'total_expenses']


class ReplenishmentSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    time = HiddenField(default=datetime.now())
    category = HiddenField(default='Пополнение')

    class Meta:
        model = Transaction
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['total_sum', 'time', 'category']
