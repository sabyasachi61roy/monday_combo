from django.urls import path
from .views import ComboList, AllAddon, AllCombo


app_name = 'products'

urlpatterns = [
    path('', ComboList.as_view(), name='combo-list'),
    path('products/combos/', AllCombo.as_view(), name="all-combos"),
    path('products/addons/', AllAddon.as_view(), name='all-addons'),
]