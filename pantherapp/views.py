from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import CustomUser
from django.contrib import messages


class HomeViews(View):
    """Обработка главной страницы"""

    template_name = 'pantherapp/index.html'

    def get(self, request):
        item = CustomUser.objects.get(pk=request.user.id)
        return render(request, self.template_name, {'item': item})


class LoginView(View):
    """Обработка страницы авторизации"""

    form_class = LoginForm
    template_name = 'pantherapp/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('pantherapp:home')
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])

            if user is not None:
                if user.is_active:
                    messages.success(request, user.username + ', Вы вошли в аккаунт!')
                    login(request, user)
                    return redirect('pantherapp:home')
            else:
                messages.error(request, 'Неверный логин или пароль. Повторите попытку')
        return redirect('pantherapp:auth')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('pantherapp:auth')