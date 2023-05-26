from django.urls import path 
from django.contrib import admin

from IllnessWeb.views import index, search

urlpatterns = [
    path('', index, name= 'index'),
    path('search/', search, name= 'search'),
    path('admin/', admin.site.urls),
]