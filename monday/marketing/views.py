from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings

from .forms import MarketingForm
from .models import Marketing
from .utils import Mailchimp
from .mixins import CsrfExemptMixin

MAILCHIMP_LIST_ID = getattr(settings, "MAILCHIMP_LIST_ID", None)
# Create your views here.
class MailchimpWebhookView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_LIST_ID):
            email = data.get('data[email]')
            hook_type = data.get('type')
            response_status, response = Mailchimp().check_subscription_status(email)
            sub_status = response['status']
            sub = None
            mailchimp_sub = None

            if sub_status == "subscribed":
                sub, mailchimp_sub = (True, True)
            elif sub_status == "unsubscribed":
                sub, mailchimp_sub = (False, False)
            if sub is not None and mailchimp_sub is not None:
                qs = Marketing.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=sub, mailchimp_subscribed=mailchimp_sub, mailchimp_msg = str(data))
            # elif sub_status == "unsubscribed":
            #     qs = Marketing.objects.filter(user__email__iexact=email)
            #     if qs.exists():
            #         qs.update(subscribed=False, mailchimp_subscribed=False, str(data))
        return HttpResponse("Thank You", staus=400)

class MarketingView(SuccessMessageMixin, UpdateView):
    form_class = MarketingForm
    template_name = 'marketing/forms.html'
    success_url = '/settings/email/'
    success_message = "Updated"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            # return HttpResponse("Not allowed", status=400)
            return redirect("/login/?next=/settings/email/")
        return super(MarketingView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Email Preferences'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = Marketing.objects.get_or_create(user=user)
        return obj