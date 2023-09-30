from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import Group
from users.forms import UserRegisterForm, UserProfileForm, UserAuthenticationForm, ResetPasswordForm

from users.models import User
from users.services import send_new_password, send_reset_password, generate_vrf_token, send_hello_and_confirm_url


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
        vrf_token = generate_vrf_token()
        confirm_url = self.request.build_absolute_uri(reverse('users:confirm', args=[vrf_token]))
        user.vrf_token = vrf_token
        user.save()

        send_hello_and_confirm_url(confirm_url, user.email)

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
def generate_new_password(request):
    new_password = generate_new_password()
    request.user.set_password(new_password)
    request.user.save()

    send_new_password(request.user.email, new_password)

    return redirect(reverse('catalog:list_product'))


def reset_password(request):
    """Сгенерировать новый пароль для пользователя если пароль забыли"""
    form = ResetPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user_email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=user_email)
            new_password = generate_new_password()
            user.set_password(new_password)
            user.save()

            send_reset_password(new_password, user_email)

            return redirect(reverse("users:login"))
        except User.DoesNotExist:
            return render(request, 'users/change_password.html', {'error_message': 'User not found'})
    return render(request, 'users/change_password.html', {'form': form})
