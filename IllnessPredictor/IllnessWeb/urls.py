from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

app_name = 'IllnessWeb'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name= 'search'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='IllnessWeb/login.html', authentication_form=LoginForm), name= 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='IllnessWeb/logout.html'), name= 'logout'),
]