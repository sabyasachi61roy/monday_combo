from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormMixin

from .forms import LoginForm, RegisterForm, ReactivateAccount
from .models import EmailActivation
from .signals import user_logged_in
from main.mixins import NextURLMixin, RequestFormMixin


# Create your views here.
@login_required
def account_home(request):
    return render(request, "accounts/home.html")

# class LoginRequiredMixin(object):
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(self, *args, **kwargs)

class AccountHome(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user
    
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(AccountHome, self).dispatch(self, *args, **kwargs)

class AccountActivate(FormMixin, View):
    success_url = '/accounts/login/'
    form_class = ReactivateAccount
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login")
                return redirect("accounts:login")
            else:
                # qs = EmailActivation.objects.filter(key__iexact=key, activated=True)
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed.
                    Do you need to <a href='{link}'>reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("accounts:login")
        context = {
            'form': self.get_form(),
            'key': key
        }
        return render(request, "registration/activation-error.html", context)
    
    def post(self, request, *args, **wargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        request = self.request
        msg = '''Activation link sent, please check your email.'''
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountActivate, self).forn_vali(form)
    
    def form_invalid(self, form):
        request = self.request
        context = {
            'form': form,
            'key': key
        }
        return render(request, "registration/activation-error.html", context)

class Register(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/login/'

class Login(NextURLMixin, RequestFormMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = "/"

    # def get_form_kwargs(self):
    #     kwargs = super(Login, self).get_form_kwargs()
    #     print(kwargs)
    #     kwargs['request'] = self.request
    #     return kwargs
    
    # def get_next_url(self):
    #     request = self.request
    #     next_ = request.GET.get('next')
    #     next_post = request.POST.get('next')
    #     redirect_path = next_ or next_post or None
    #     if is_safe_url(redirect_path, request.get_host()):
    #         return redirect_path
    #     return "/"

    def form_valid(self, form):
        # user = form.user
        # if user.is_autenticated:
        #     # user_logged_in.send(user.__class__, instance=user, request=request)
        #     next_path = self.get_next_url()
        #     return redirect(next_path)
        # return super(Login, self).form_invalid(form)
        next_path = self.get_next_url()
        return redirect(next_path)

    # def form_valid(self, form):
    #     request = self.request
    #     next_ = request.GET.get('next')
    #     next_post = request.POST.get('next')
    #     redirect_path = next_ or next_post or None
    #     email = form.cleaned_data.get('email')
    #     password = form.cleaned_data.get('password')
    #     user = authenticate(request, email=email, password=password)
    #     if user is not None:
    #         if not user.is_active:
    #             messages.error(request, "This account is inactive")
    #             return super(Login, self).form_invalid(form)
    #         login(request, user)
    #         if is_safe_url(redirect_path, request.get_host()):
    #             return redirect(redirect_path)
    #         else:
    #             return redirect("/")
    #     return super(Login, self).form_invalid(form)


# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         email = form.cleaned_data.get('email')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             print("Error")
#     return render(request, "accounts/login.html", context)

# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     if form.is_valid():
#         form.save()
#     return render(request, "accounts/register.html", context)