import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TestSignupView(TestCase):
    """Test SignupView"""

    def setUp(self):
        # Note: Use -v 3 option!
        print("# {} is running!".format(self.id()))
        self.user = get_user_model().objects.create_user(
            email='admin@example.com',
            password='password',
            is_active=True)
        self.activate_user = get_user_model().objects.create_user(
            email='activate@example.com',
            password='password', )

    def tearDown(self):
        print("# {} is finished!".format(self.id()))
        get_user_model().objects.filter(email='admin@example.com').delete()
        get_user_model().objects.filter(email='activate@example.com').delete()

    def test_get_success(self):
        """
        Get /register/
        Template: /user/signup.html
        """
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].errors)
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_get_by_authenticated_user(self):
        """
        Get /signup/ with login info in cookie
        Template /product/index.html
        """
        logged_in = self.client.login(email=self.user.email, password='password')
        self.assertTrue(logged_in)
        response = self.client.get('/signup/')
        self.assertRedirects(response, '/products')

    def test_post_success(self):
        """
        Post: /signup/
        Case: create new user
        """
        response = self.client.post('/signup/', {
            'email': 'user@example.com',
            'postal_code': '150-0000',
            'name': 'テスト 太郎',
            'address': '東京都品川区東品川1-1-23',
            'phone': '070-0000-0000',
            'password': 'password',
            'password2': 'password',
        })
        self.assertTemplateUsed(response, 'user/verify.html')
        self.assertTrue(get_user_model().objects.filter(email='user@example.com').exists())

    def test_post_with_same_email(self):
        """
        Post: /signup/
        Case: user already exists error
        """
        response = self.client.post('/signup/', {
            'email': self.user.email,
            'postal_code': '150-0000',
            'name': 'テスト 山田',
            'address': '東京都品川区東品川1-1-23',
            'phone': '070-0000-0000',
            'password': 'password',
            'password2': 'password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'この メールアドレス を持った User が既に存在します。')
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertFalse(get_user_model().objects.filter(name='テスト 山田').exists())

    def test_post_signup_validation(self):
        """
        Post: /signup/
        Case: face validation error
        """
        response = self.client.post('/signup/', {
            'email': self.user.email,
            'postal_code': '150-000',
            'name': 'テスト 山田',
            'address': '東京都品川区東品川1-1-23',
            'phone': '070-0000-000',
            'password': 'passwor',
            'password2': 'passwr',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'postal_code', '郵便番号が仕様(150-0000)と異なります。')
        self.assertFormError(response, 'form', 'phone', '電話番号が仕様(090-0000-0000/03-0000-0000)と異なります。')
        self.assertFormError(response, 'form', 'password', '8文字以上で入力してください')
        self.assertFormError(response, 'form', None, 'パスワードと確認用パスワードが合致しません')
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertFalse(get_user_model().objects.filter(name='テスト 山田').exists())

    def test_activate_success(self):
        """
        Get: /activate/{emailb64}/{token}
        Case: activate success
        """
        token = default_token_generator.make_token(self.activate_user)
        emailb64 = urlsafe_base64_encode(force_bytes(self.activate_user.email))
        response = self.client.get(f'/activate/{emailb64}/{token}/')
        self.assertTemplateUsed(response, 'user/complete_confirmation.html')

    def test_activate_with_wrong_token(self):
        """
        Get: /activate/{emailb64}/{token}
        Case: activate failed because of wrong token
        """
        token = uuid.uuid4()
        emailb64 = urlsafe_base64_encode(force_bytes(self.activate_user.email))
        response = self.client.get(f'/activate/{emailb64}/{token}/')
        self.assertTemplateUsed(response, 'user/verify.html')

    def test_activate_with_wrong_emailb64(self):
        """
        Get: /activate/{emailb64}/{token}
        Case: activate failed because of wrong emailb64
        """
        token = default_token_generator.make_token(self.user)
        emailb64 = uuid.uuid4()
        response = self.client.get(f'/activate/{emailb64}/{token}/')
        self.assertTemplateUsed(response, 'user/verify.html')


class LoginViewTest(TestCase):

    def setUp(self) -> None:
        print("# {} is running!".format(self.id()))
        self.user = get_user_model().objects.create_user(
            email='admin@example.com',
            password='password',
            is_active=True)

    def tearDown(self) -> None:
        print("# {} is finished!".format(self.id()))
        get_user_model().objects.filter(email='admin@example.com').delete()

    def test_get_login_template(self):
        """
        GET: /login/
        CASE: success
        """
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'user/login.html')

    def test_get_login_with_authenticated_user(self):
        """
        GET: /login/
        CASE: redirected to products index
        """
        logged_in = self.client.login(email=self.user.email, password='password')
        self.assertTrue(logged_in)
        response = self.client.get('/login/')
        self.assertRedirects(response, '/products')

    def test_post_login_success(self):
        """
        POST: /login/
        CASE: login success
        """
        response = self.client.post('/login/', {
            'email': self.user.email,
            'password': 'password', })
        self.assertRedirects(response, '/products')

    def test_post_login_validation(self):
        """
        POST: /login/
        CASE: login failed because of wrong password
        """
        response = self.client.post('/login/', {
            'email': self.user.email,
            'password': 'password1', })
        self.assertFormError(response, 'form', None, '正しいメールアドレスとパスワードを入力してください')
        self.assertTemplateUsed(response, 'user/login.html')

    def test_post_login_with_inactivated_user(self):
        """
        POST: /login/
        CASE: login failed because of wrong email
        """
        response = self.client.post('/login/', {
            'email': self.user.email+'1',
            'password': 'password', })
        self.assertFormError(response, 'form', None, '正しいメールアドレスを入力してください')
        self.assertTemplateUsed(response, 'user/login.html')


class LogoutView(TestCase):
    def setUp(self) -> None:
        print("# {} is running!".format(self.id()))
        self.user = get_user_model().objects.create_user(
            email='admin@example.com',
            password='password',
            is_active=True)

    def tearDown(self) -> None:
        print("# {} is finished!".format(self.id()))
        get_user_model().objects.filter(email='admin@example.com').delete()

    def test_logout(self):
        """
        GET /logout/
        CASE logout success
        """
        logged_in = self.client.login(email=self.user.email, password='password')
        self.assertTrue(logged_in)
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')


class PasswordResetViewTest(TestCase):
    def setUp(self) -> None:
        print("# {} is running!".format(self.id()))
        self.user = get_user_model().objects.create_user(
            email='admin@example.com',
            password='password',
            is_active=True)

    def tearDown(self) -> None:
        print("# {} is finished!".format(self.id()))
        get_user_model().objects.filter(email='admin@example.com').delete()

    def test_get_success(self):
        """
        GET /reset/
        CASE reset success
        """
        response = self.client.get('/reset/')
        self.assertTemplateUsed(response, 'user/reset_password.html')

    def test_post_reset_success(self):
        """
        POST /reset/
        CASE reset success
        """
        response = self.client.post('/reset/', {'email': self.user.email})
        self.assertTemplateUsed(response, 'user/reset_password.html')

    def test_post_reset_validation(self):
        """
        POST /reset/
        CASE reset failed because of wrong email
        """
        response = self.client.post('/reset/', {'email': self.user.email + '1'})
        self.assertFormError(response, 'form', None, '正しいメールアドレスを入力してください')
        self.assertTemplateUsed(response, 'user/reset_password.html')


class PasswordEditViewTest(TestCase):
    def setUp(self) -> None:
        print("# {} is running!".format(self.id()))
        self.user = get_user_model().objects.create_user(
            email='admin@example.com',
            password='password',
            is_active=True)

    def tearDown(self) -> None:
        print("# {} is finished!".format(self.id()))
        get_user_model().objects.filter(email='admin@example.com').delete()

    def test_post_success(self):
        """
        POST /edit/password/
        CASE success
        """
        emailb64 = urlsafe_base64_encode(force_bytes(self.user.email))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(f'/edit/password/{emailb64}/{token}/')
        self.assertTemplateUsed(response, 'user/edit_password.html')
        response = self.client.post('/edit/password/', {
            'password': 'password1',
            'password2': 'password1',
            'emailb64': emailb64,
            'token': token, })
        self.assertTemplateUsed(response, 'user/complete_confirmation.html')

    def test_post_failed_by_password_length_validation(self):
        """
        POST /edit/password/
        CASE success
        """
        emailb64 = urlsafe_base64_encode(force_bytes(self.user.email))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(f'/edit/password/{emailb64}/{token}/')
        self.assertTemplateUsed(response, 'user/edit_password.html')
        response = self.client.post('/edit/password/', {
            'password': 'passwor',
            'password2': 'password',
            'emailb64': emailb64,
            'token': token, })
        self.assertFormError(response, 'form', None, '8文字以上で入力してください')
        self.assertTemplateUsed(response, 'user/edit_password.html')

    def test_post_failed_by_password_validation(self):
        """
        POST /edit/password/
        CASE success
        """
        emailb64 = urlsafe_base64_encode(force_bytes(self.user.email))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(f'/edit/password/{emailb64}/{token}/')
        self.assertTemplateUsed(response, 'user/edit_password.html')
        response = self.client.post('/edit/password/', {
            'password': 'password',
            'password2': 'password1',
            'emailb64': emailb64,
            'token': token, })
        self.assertFormError(response, 'form', None, 'パスワードが一致しません')
        self.assertTemplateUsed(response, 'user/edit_password.html')
