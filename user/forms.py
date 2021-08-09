import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from .models import User

POSTAL_REGEXP = re.compile('[1-9][0-9]{2}-[0-9]{4}')
POSTAL_MESSAGE = '郵便番号が仕様(150-0000)と異なります。'
PHONE_REGEXP = re.compile('([0-9]{3}-[0-9]{4}-[0-9]{4}|[0-9]{2}-[0-9]{4}-{0-9]{4})')
PHONE_MESSAGE = '電話番号が仕様(090-0000-0000/03-0000-0000)と異なります。'


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'postal_code', 'address', 'phone', )

    password2 = forms.CharField(
        label='確認用パスワード',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # フィールドの属性を書き換え
        self.fields['email'].required = True
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}

    def clean_email(self):
        value = self.cleaned_data['email']
        return value

    def clean_postal_code(self):
        value = self.cleaned_data['postal_code']
        if not POSTAL_REGEXP.match(value):
            raise forms.ValidationError(POSTAL_MESSAGE)
        return value

    def clean_phone(self):
        value = self.cleaned_data['phone']
        if not PHONE_REGEXP.match(value):
            raise forms.ValidationError(PHONE_MESSAGE)
        return value

    def clean_password(self):
        value = self.cleaned_data['password']
        if 8 > len(value):
            raise forms.ValidationError('%(min_length)s文字以上で入力してください', params={'min_length': 8})
        return value

    def clean(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('パスワードと確認用パスワードが合致しません')
        # ユニーク制約を自動でバリデーションしてほしい場合は super の clean() を明示的に呼び出す
        super().clean()


class LoginForm(forms.Form):
    """ログイン画面用のフォーム"""

    email = forms.CharField(
        label=_('メールアドレス'),
        widget=forms.TextInput(attrs={'placeholder': 'メールアドレス', 'autofocus': True}),
    )
    password = forms.CharField(
        label=_('パスワード'),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}, render_value=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean_password(self):
        value = self.cleaned_data['password']
        return value

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = get_user_model().objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('正しいメールアドレスを入力してください')
        # パスワードはハッシュ化されて保存されているので平文での検索はできない
        if not user.check_password(password):
            raise forms.ValidationError("正しいメールアドレスとパスワードを入力してください")
        # 取得したユーザーオブジェクトを使い回せるように内部に保持しておく
        self.user_cache = user

    def get_user(self):
        return self.user_cache


class PasswordResetForm(forms.Form):
    email = forms.CharField(label=_('メールアドレス'), widget=forms.TextInput(attrs={'placeholder': 'メールアドレス', 'autofocus': True}),)

    def clean(self):
        email = self.cleaned_data.get('email')
        try:
            user = get_user_model().objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('正しいメールアドレスを入力してください')


class PasswordEditForm(forms.Form):

    password = forms.CharField(label='確認用パスワード', required=True,)
    password2 = forms.CharField(label='確認用パスワード', required=True,)
    emailb64 = forms.CharField(required=True)
    token = forms.CharField(required=True)

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if 8 > len(password):
            raise forms.ValidationError('%(min_length)s文字以上で入力してください', params={'min_length': 8})
        if password != password2:
            raise forms.ValidationError('パスワードが一致しません')
