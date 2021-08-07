from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase


class TestUser(TestCase):

    def setUp(self):
        # Note: Use -v 3 option!
        print("# {} is running!".format(self.id()))
        self.user = get_user_model().objects.create_user(email='user@user.com', password='Password', name='')

    def tearDown(self):
        user = get_user_model().objects.get(pk=self.user.id)
        user.delete()

    def test_post_login(self):
        """
        test login count method
        """
        self.assertEqual(self.user.login_count, 0)
        self.user.post_login()
        # verify after login
        self.assertEqual(self.user.login_count, 1)
        self.assertEqual(get_user_model().objects.get(pk=self.user.id).login_count, 1)

    def test_activate_user(self):
        """
        test login count method
        """
        self.assertEqual(self.user.is_active, False)
        self.user.activate_user()
        # verify after login
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(get_user_model().objects.get(pk=self.user.id).is_active, True)

    def test_send_verify_mail(self):
        self.assertEqual(len(mail.outbox), 0)
        self.user.send_verify_mail(current_site='localhost:8000')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate your account.')

    def test_send_reset_password_mail(self):
        self.assertEqual(len(mail.outbox), 0)
        self.user.send_reset_password_mail(current_site='localhost:8000')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reset your password.')
