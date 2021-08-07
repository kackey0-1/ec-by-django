import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View

from .forms import LoginForm, SignupForm, PasswordResetForm, PasswordEditForm

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class SignupView(View):
    def get(self, request, *args, **kwargs):
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        context = {
            'form': SignupForm(),
        }
        return render(request, 'user/signup.html', context)

    def post(self, request, *args, **kwargs):
        logger.info("You're in post!!!")
        form = SignupForm(request.POST)
        if not form.is_valid():
            return render(request, 'user/signup.html', {'form': form})
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        current_site = get_current_site(request).domain
        user.send_verify_mail(current_site)
        return render(request, 'user/verify.html')


def activate(request, emailb64, token):
    try:
        email = urlsafe_base64_decode(emailb64).decode()
        user = UserModel.objects.get(email=email)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.activate_user()
        return render(request, 'user/complete_confirmation.html')
    else:
        messages.error(request, 'メールアドレスが有効ではありません。')
        logger.info(messages)
        return render(request, 'user/verify.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """GETリクエスト用のメソッド"""
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(reverse('product:index'))

        context = {
            'form': LoginForm(),
        }
        return render(request, 'user/login.html', context)

    def post(self, request, *args, **kwargs):
        """POSTリクエスト用のメソッド"""
        # リクエストからフォームを作成
        form = LoginForm(request.POST)
        # バリデーション（ユーザーの認証も合わせて実施）
        if not form.is_valid():
            # バリデーションNGの場合はログイン画面のテンプレートを再表示
            return render(request, 'user/login.html', {'form': form})
        # ユーザーオブジェクトをフォームから取得
        user = form.get_user()
        if not user.is_active:
            messages.error(request, "ユーザーが有効化されていません。")
            return render(request, 'user/login.html', {'form': form})
        # ログイン処理（取得したユーザーオブジェクトをセッションに保存 & ユーザーデータを更新）
        auth_login(request, user)
        user.post_login()
        # ロギング
        logger.info("User(id={}) has logged in.".format(user.id))
        # フラッシュメッセージを画面に表示
        messages.info(request, "ログインしました。")
        # ショップ画面にリダイレクト
        return redirect(reverse('product:index'))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # ロギング
            logger.info("User(id={}) has logged out.".format(request.user.id))
            # ログアウト処理
            auth_logout(request)
            # フラッシュメッセージを画面に表示
            messages.info(request, "ログアウトしました。")
        return redirect(reverse('user:login'))


class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': PasswordResetForm(), }
        return render(request, 'user/reset_password.html', context)

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if not form.is_valid():
            return render(request, 'user/reset_password.html', {'form': form})
        user = UserModel.objects.get(email=form.cleaned_data['email'])
        current_site = get_current_site(request).domain
        user.send_reset_password_mail(current_site)
        messages.info(request, 'パスワードリセット用のリンクをメールにて送信しました。')
        return render(request, 'user/reset_password.html', {'form': form})


class PasswordEditView(View):
    def get(self, request, emailb64, token, *args, **kwargs):
        context = {
            'form': PasswordEditForm(),
            'emailb64': emailb64,
            'token': token, }
        return render(request, 'user/edit_password.html', context)

    def post(self, request, *args, **kwargs):
        form = PasswordEditForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form,
                'emailb64': form.cleaned_data['emailb64'],
                'token': form.cleaned_data['token'], }
            return render(request, 'user/edit_password.html', context)
        try:
            email = urlsafe_base64_decode(form.cleaned_data['emailb64']).decode()
            user = UserModel.objects.get(email=email)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, form.cleaned_data['token']):
            user.set_password(form.cleaned_data['password'])
            user.activate_user()
            return render(request, 'user/complete_confirmation.html')
        else:
            messages.error(request, 'トークンが有効ではありません。')
            logger.info(messages)
            return render(request, 'user/reset_password.html')

