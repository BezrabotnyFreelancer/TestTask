from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Profile, Transaction
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['user', 'balance']


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'user']


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ['user', 'total_sum', 'time']
