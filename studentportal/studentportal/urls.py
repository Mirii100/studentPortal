
from django.contrib import admin
from django.urls import path,include
from dashboard import  views as dash_views
urlpatterns = [
    path('',include('dashboard.urls')),
    path('register/',dash_views.register,name='register'),
    path('admin/', admin.site.urls),
    

]
