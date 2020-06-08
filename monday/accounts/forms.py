# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.contrib.auth import authenticate, login
from django.contrib import messages

from .signals import user_logged_in
from .models import User, EmailActivation

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        qs = User.objects.filter(email=email)
        if qs.exists():
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse("accounts:resend-activate")
                reconfirm_msg = """<a href='{resend_link}'>click here.</a>
                """.format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg = "To resend confirmation email" + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg))
                email_confirm_qs = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_qs:
                    raise forms.ValidationError(mark_safe("You email is not confirmed. Please check your email or " + reconfirm_msg + "to resend confirmation email."))
                if not is_confirmable and not email_confirm_qs:
                    raise forms.ValidationError("User inactive")

        user = authenticate(request, email=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid Credentials")
        login(request, user)
        self.user = user
        user_logged_in.send(user.__class__, instance=user, request=request)
        return data

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

class RegisterForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # obj, is_created = EmailActivation.objects.create(user=user)
        # obj.send_activation_email()
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(label="Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = User
        fields = ['full_name',]

class ReactivateAccount(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            reset_link = reverse("accounts:register")
            msg = """This email does not exists!
            Register a <a href='{link}'>new account</a>?
            """.format(link=reset_link)
            raise forms.ValidationError(mark_safe(msg))
        return email