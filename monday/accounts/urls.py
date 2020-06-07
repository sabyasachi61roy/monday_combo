from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

app_name = 'accounts'

urlpatterns = [
    # path('register/', register_page, name='register'),
    path('register/', Register.as_view(), name='register'),
    # path('login/', login_page, name='login'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', AccountHome.as_view(), name='account-home'),
]