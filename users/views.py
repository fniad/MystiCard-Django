import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import Group
from users.forms import UserRegisterForm, UserProfileForm, UserAuthenticationForm, ResetPasswordForm

from users.models import User


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'users/login.html'
    success_url = 'catalog:list_product'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_class(self):
        return self.authentication_form or self.form_class


class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        characters = string.ascii_letters + string.digits + string.punctuation
        vrf_token = ''.join(random.choice(characters) for _ in range(12))
        confirm_url = self.request.build_absolute_uri(reverse('users:confirm', args=[vrf_token]))
        user.vrf_token = vrf_token
        user.save()

        send_mail(
            subject='Поздравляем с регистрацией на сайте MailMagic',
            message=f'Пожалуйста, подтвердите свою электронную почту по ссылке {confirm_url}.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class ConfirmRegistrationView(View):
    def get(self, request, vrf_token):
        try:
            user = User.objects.get(vrf_token=vrf_token)
            user.is_active = True
            user.vrf_token = None
            group = Group.objects.get(name='users')
            user.groups.set([group])
            user.save()
        except User.DoesNotExist:
            messages.error(request,
                           "Ошибка: Пользователь с указанным токеном не найден. Пройдите регистрацию снова.")
        return redirect('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def generate_new_password(request, length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(random.choice(characters) for _ in range(length))

    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )

    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:list_product'))


def reset_password(request):
    """Сгенерировать новый пароль для пользователя если пароль забыли"""
    form = ResetPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user_email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=user_email)
            characters = string.ascii_letters + string.digits + string.punctuation
            new_password = ''.join(random.choice(characters) for _ in range(12))
            user.set_password(new_password)
            user.save()

            subject = "Смена пароля на сайте MailMagic"
            message = f"Ваш новый пароль: {new_password}"
            from_email = settings.EMAIL_HOST_USER
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[user_email]
            )
            return redirect(reverse("users:login"))
        except User.DoesNotExist:
            return render(request, 'users/change_password.html', {'error_message': 'User not found'})
    return render(request, 'users/change_password.html', {'form': form})
