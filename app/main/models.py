from django.db import models
from uuid import uuid4
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

STANDARD_CATS = ("Забота о себе",
                 "Зарплата",
                 "Здоровье и фитнес",
                 "Кафе и рестораны",
                 "Машина",
                 "Образование",
                 "Отдых и развлечения",
                 "Платежи, комиссии",
                 "Покупки: одежда, техника",
                 "Продукты",
                 "Проезд"
                 )


class Category(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Category')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-name']

    @receiver(post_save, sender=get_user_model())
    def create_cats_for_user(sender, instance, created, **kwargs):
        if created:
            for default_cat in STANDARD_CATS:
                cat = Category.objects.create(user=instance, name=default_cat)
                cat.save()


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total_sum = models.FloatField(verbose_name='Transaction_sum', help_text='Введите сумму транзакции')
    time = models.DateTimeField(verbose_name='Date_of_transaction', help_text='Введите дату транзакции')
    category = models.CharField(max_length=100, verbose_name='Category')

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-time']


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    balance = models.FloatField(verbose_name='Balance', default=0.0)
    total_expenses = models.FloatField(verbose_name='Total_expenses', default=0.0)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @receiver(post_save, sender=get_user_model())
    def create_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = Profile.objects.create(user=instance)
            new_profile.save()

    @receiver(post_save, sender=Transaction)
    def update_profile(sender, instance, created, **kwargs):
        if created:
            profile = Profile.objects.get(user=instance.user)
            if instance.category == 'Пополнение':
                profile.balance += instance.total_sum
                profile.save()
            else:
                profile.balance -= instance.total_sum
                profile.total_expenses += instance.total_sum
                profile.save()
