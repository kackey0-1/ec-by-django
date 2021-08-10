# import os
#
# import chromedriver_binary
# from django.contrib.auth import get_user_model
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium import webdriver
#
#
# class TestLoginSenario(StaticLiveServerTestCase):
#     """Login Senario
#     https://chromedriver.chromium.org/downloads
#     """
#     SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         # エラー時のスクリーンショット格納ディレクトリを作成
#         os.makedirs(cls.SCREENSHOT_DIR, exist_ok=True)
#
#         # Note: ChromeDriverのパスを通すためにimportが必要
#         print(chromedriver_binary.chromedriver_filename)
#         chrome_options = webdriver.ChromeOptions()
#         # headlessモード
#         # chrome_options.add_argument('--headless')
#         cls.selenium = webdriver.Chrome(chrome_options=chrome_options)
#         cls.selenium.implicitly_wait(5)
#
#     def setUp(self):
#         super().setUp()
#         self.user = get_user_model().objects.create_superuser(email='admin@example.com',
#                                                               password='password',
#                                                               is_active=True,)
#         if os.path.exists(self._get_screenshot_filepath()):
#             os.remove(self._get_screenshot_filepath())
#
#     def tearDown(self):
#         self.selenium.save_screenshot(self._get_screenshot_filepath())
#         # take screenshots if error occurs
#         for method, error in self._outcome.errors:
#             if error:
#                 self.selenium.save_screenshot(self._get_screenshot_filepath())
#                 break
#         super().tearDown()
#
#     @classmethod
#     def tearDownClass(cls):
#         # Note: If ChromeDriver with headless mode
#         #       must execute tearDownClassでcls.selenium.quit()
#         cls.selenium.quit()
#         super().tearDownClass()
#
#     def _get_screenshot_filepath(self):
#         return os.path.join(self.SCREENSHOT_DIR, '{}.png'.format(self.id()))
#
#     def test_login(self):
#         self.selenium.get('{}{}'.format(self.live_server_url, '/login/'))
#         username_input = self.selenium.find_element_by_name('email')
#         username_input.send_keys(self.user.email)
#         password_input = self.selenium.find_element_by_name('password')
#         password_input.send_keys('password')
#         self.selenium.find_element_by_xpath('//input[@value="ログイン"]').click()
#         self.assertEqual(self.selenium.title, 'Product Index')
