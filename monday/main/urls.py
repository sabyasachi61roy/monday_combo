"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from carts.views import cart_api
from marketing.views import MarketingView, MailchimpWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('products.urls', namespace='products')),
    path('carts/cart/api/', cart_api, name="cart-api"),
    path('carts/', include('carts.urls', namespace='carts')),
    path('carts/checkout/', include('deliverypoints.urls', namespace='deliverypoints')),
    path('carts/checkout/', include('address.urls', namespace='address')),
    path('search/', include("search.urls", namespace='search')),
    path('settings/email/', MarketingView.as_view(), name="marketing"),
    path('webhook/maichimp/', MailchimpWebhookView.as_view(), name="webhook-mailchimp"),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)