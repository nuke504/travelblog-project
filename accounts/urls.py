from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('change_password', views.change_password, name='change_password'),
    path('logout', views.logout, name='logout'),
    path('<int:blogger_id>', views.profile, name='profile'),
]