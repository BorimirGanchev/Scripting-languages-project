from django.urls import path 
from django.contrib import admin

from IllnessWeb.views import index

urlpatterns = [
    path('', index, name= 'index'),
    path('admin/', admin.site.urls),
]