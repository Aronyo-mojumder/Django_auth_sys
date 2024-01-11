from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('conf_email_sent/<uidb64>/<token>/', views.conf_email_sent, name='conf_email_sent'),  # Updated URL name
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('home/', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
]
