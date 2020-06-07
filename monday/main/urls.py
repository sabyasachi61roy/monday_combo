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
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from carts.views import cart_api
from marketing.views import MarketingView, MailchimpWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('accounts.passwords.urls')),
    path('', include('products.urls', namespace='products')),
    path('carts/cart/api/', cart_api, name="cart-api"),
    path('carts/', include('carts.urls', namespace='carts')),
    path('carts/checkout/', include('deliverypoints.urls', namespace='deliverypoints')),
    path('carts/checkout/', include('address.urls', namespace='address')),
    path('search/', include("search.urls", namespace='search')),
    path('settings/email/', MarketingView.as_view(), name="marketing"),
    path('webhook/maichimp/', MailchimpWebhookView.as_view(), name="webhook-mailchimp"),

    # url(r'^accounts/password/change/$', 
    #         auth_views.PasswordChangeView.as_view(), 
    #         name='password_change'),
    # url(r'^accounts/password/change/done/$',
    #         auth_views.PasswordChangeDoneView.as_view(), 
    #         name='password_change_done'),
    # url(r'^accounts/password/reset/$', 
    #         auth_views.PasswordResetView.as_view(), 
    #         name='password_reset'),
    # url(r'^accounts/password/reset/done/$', 
    #         auth_views.PasswordResetDoneView.as_view(), 
    #         name='password_reset_done'),
    # url(r'^accounts/password/reset/\
    #         (?P<uidb64>[0-9A-Za-z_\-]+)/\
    #         (?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
    #         auth_views.PasswordResetConfirmView.as_view(), 
    #         name='password_reset_confirm'),

    # url(r'^accounts/password/reset/complete/$', 
    #         auth_views.PasswordResetCompleteView.as_view(), 
    #         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)