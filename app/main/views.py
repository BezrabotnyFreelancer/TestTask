from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime, time
# Create your views here.
from .models import Category, Transaction, Profile
from .profile_methods import get_main_profile
from .forms import ReplenishmentForm, FilterForm, TransactionCreationForm, CategoryCreationForm
from .template_pack import TEMPLATES as templ


USERS = get_user_model().objects.all()
if datetime.now().time() == time(9, 0, 0, 0):
    for i in USERS:
        balance = Profile.objects.get(user=i)
        transactions = Transaction.objects.filter(user=i)
        verified_transactions = [x.total_sum for x in transactions if x.category != 'Пополнение']
        average = round(sum(verified_transactions) / len(verified_transactions), 2)
        msg = f"Ваш баланс равен {balance.balance} Среднее сумма транзакций {average} руб."
        send_mail('Статистика', msg, settings.EMAIL_HOST_USER, [i.email])


@login_required(login_url='account_login')
def main_profile(request):
    return render(request, templ.get('profile').get('info'), context={'profile': get_main_profile(request)})


@login_required(login_url='account_login')
def replenishment(request):
    profile = get_main_profile(request)
    if request.method == 'POST':
        replenishment_form = ReplenishmentForm(request.POST)
        if replenishment_form.is_valid():
            transaction = Transaction()
            transaction.user = request.user
            transaction.total_sum = float(replenishment_form.cleaned_data['replenishment'])
            transaction.time = datetime.now()
            transaction.category = 'Пополнение'
            transaction.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, templ.get('profile').get('replenishment'), {'form': replenishment_form})
    else:
        replenishment_form = ReplenishmentForm()
        return render(request, templ.get('profile').get('replenishment'),
                      {'form': replenishment_form, 'profile': profile})


@login_required(login_url='account_login')
def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    if request.method == 'POST':
        filter_form = FilterForm(request.POST)

        if filter_form.is_valid():
            filter_transactions = filter_form.cleaned_data['filter_choice']
            filter_flag = '' if filter_form.cleaned_data['flag_choice'] else '-'
            transactions = Transaction.objects.filter(user=request.user).order_by(f'{filter_flag}{filter_transactions}')
            return render(request, templ.get('transactions').get('list'),
                          {'transactions': transactions, 'form': filter_form})
        else:
            return render(request, templ.get('transactions').get('list'),
                          {'transactions': transactions, 'form': filter_form})
    else:
        form = FilterForm()
        return render(request, templ.get('transactions').get('list'), {'form': form, 'transactions': transactions})


@login_required(login_url='account_login')
def create_transaction(request):
    categories = [(x.name, x.name) for x in Category.objects.filter(user=request.user)]
    if request.method == 'POST':
        transaction_form = TransactionCreationForm(request.POST)
        transaction_form.fields['category'].choices = categories
        if transaction_form.is_valid():
            transaction = Transaction()
            transaction.user = request.user
            transaction.total_sum = float(transaction_form.cleaned_data['total_sum'])
            transaction.time = transaction_form.cleaned_data['time']
            transaction.category = transaction_form.cleaned_data['category']
            transaction.save()
            return HttpResponseRedirect(reverse('transaction_list'))
        else:
            return render(request, templ.get('transactions').get('create'),
                          {'form': transaction_form, 'categories': categories})
    else:
        form = TransactionCreationForm()
        form.fields['category'].choices = categories
        return render(request, templ.get('transactions').get('create'), {'form': form, 'categories': categories})


@login_required(login_url='account_login')
def category_list_and_create(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        category_form = CategoryCreationForm(request.POST)
        if category_form.is_valid():
            new_category = Category()
            new_category.user = request.user
            new_category.name = category_form.cleaned_data['name']
            new_category.save()
            return HttpResponseRedirect(reverse('categories'))
        else:
            return render(request, templ.get('category').get('list'), {'categories': categories, 'form': category_form})
    else:
        form = CategoryCreationForm()
        return render(request, templ.get('category').get('list'), {'form': form, 'categories': categories})


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ('name', )
    template_name = templ.get('category').get('update')
    login_url = reverse_lazy('account_login')
    success_url = reverse_lazy('categories')

    def test_func(self):
        category = self.get_object()
        return category.user == self.request.user


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    login_url = reverse_lazy('account_login')
    template_name = templ.get('category').get('update')
    success_url = reverse_lazy('categories')

    def test_func(self):
        category = self.get_object()
        return category.user == self.request.user
