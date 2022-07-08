from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'pantherapp'

urlpatterns = [
    path('', login_required(views.HomeViews.as_view()), name='home'),
    path('login/', views.LoginView.as_view(), name='auth'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]