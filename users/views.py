from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from orders.models import Order, OrderItem
# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile'))
            else:
                # Добавляем ошибку если пользователь не найден
                form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = UserLoginForm()  # Создаем форму для GET запроса

    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        print("Form is valid:", form.is_valid())
        print("Form errors:", form.errors)
        if form.is_valid():
            user = form.save() 
            auth.login(request, user)
            messages.success(request, f'{user.username}, has successful registration')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)  # Исправлено

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was changed')
            return HttpResponseRedirect(reverse('users:profile'))  # Исправлен namespace
    else:
        form = ProfileForm(instance=request.user)  # Исправлено
    
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.select_related('product')
        )
    ).order_by('-id')
    return render(request, 'users/profile.html', {'form': form, 'orders': orders})

def logout(request):
    auth.logout(request)
    return redirect('main:popular_list')
