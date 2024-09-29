import secrets
import string
import random

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegistrationForm
from users.models import User
from django.contrib import messages


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('catalog:home')

    def form_invalid(self, form):
        print(form.error_messages)
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтвереждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'

    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        new_password = self.generate_random_password()
        user.password = make_password(new_password)
        user.save()
        self.send_password_email(email, new_password)

        messages.success(self.request, 'A new password has been sent to your email.')
        return redirect(self.success_url)

    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def send_password_email(self, email, new_password):
        send_mail(
            'Your New Password',
            f'Your new password is: {new_password}',
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    def get(self, request, *args, **kwargs):
        print("Using custom password reset done template")
        return super().get(request, *args, **kwargs)
