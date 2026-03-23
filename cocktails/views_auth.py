from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from cocktails.models import Client


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Такой пользователь уже существует!')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        Client.objects.create(user=user, name=username, balance=0)
        login(request, user)
        return redirect('index')

    return render(request, 'cocktails/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')
            return redirect('login')

    return render(request, 'cocktails/login.html')


def logout_view(request):
    response = redirect('login')  # после выхода отправляем на страницу логина
    logout(request)

    # Сбрасываем все cookies (кроме служебных Django)
    for key in request.COOKIES:
        response.delete_cookie(key)

    messages.success(request, "Вы успешно вышли из системы.")
    return response
