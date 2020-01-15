from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class LoginTest(StaticLiveServerTestCase):

# Init and teardown section
    @classmethod
    def setUpClass(cls):
        super(LoginTest, cls).setUpClass()
        cls.selenium = WebDriver(executable_path="./blogapp/tests/webdriver/geckodriver")
        cls.selenium.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LoginTest, cls).tearDownClass()

# Test cases section

    def test_login_with_valid_creds(self):
        """
        1. Open home page
        2. Click 'login' link
        3. Assert page is 'login'
        4. Enter valid login name
        5. Enter valid pass
        6. Click 'login'
        7. Assert page is home
        8. Assert user is logged in by name in the header
        """
        driver = self.selenium
        driver.get(self.live_server_url)
        assert 'Home' in driver.title
