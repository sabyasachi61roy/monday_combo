from django.urls import path
from .views import ComboList


app_name = 'products'

urlpatterns = [
    path('', ComboList.as_view(), name='combo-list'),
]