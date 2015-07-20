from django.test import TestCase

# for Selenium testing
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from growthstreet.models import LoanRequest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestLoanRequest(TestCase):

    @classmethod
    def setUpClass(cls):
        # creating 2 users
        usernames = [['testuser1', 'nj1411@ic.ac.uk'],
                     ['superuser1', 'namanjn07@hotmail.com']]

        for i, email in usernames:
            a = User.objects.create_user(username=i, password=i, email=email)
            a.is_active = True
            if i == 'superuser1':
                a.is_staff = True
                a.is_superuser = True
            a.save()

        cls.testuser1 = User.objects.filter(username='testuser1')[0]

    def testRequestLoan(self):

        requests = LoanRequest.objects.all()
        self.assertEqual(len(requests), 0)

        # Creating a LoanRequest
        reason, amount, loanTime = "mortgage", 10000, 2
        request = LoanRequest(reason=reason, amount=amount, loanTime=loanTime, user=self.testuser1)
        request.save()

        requests = LoanRequest.objects.all()

        self.assertEqual(len(requests), 1)
        self.assertEqual(len(self.testuser1.loanrequest_set.all()), 1)

    def testRequestLoanOutOfBounds(self):

        requests = LoanRequest.objects.all()
        self.assertEqual(len(requests), 0)

        # Creating a LoanRequest
        reason, amount, loanTime = "mortgage", 100, 2
        request = LoanRequest(reason=reason, amount=amount, loanTime=loanTime, user=self.testuser1)

        # This should raise a Validation Error
        self.assertRaises(ValidationError, request.save)

    @classmethod
    def tearDownClass(cls):
        pass


class TestUI(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):

        # Creating 1 user.
        usernames = [['testuser2', 'nj1411@ic.ac.uk']]

        for i, email in usernames:
             a = User.objects.create_user(username=i, password=i, email=email)
             a.is_active = True
             a.save()

        cls.testuser2 = User.objects.filter(username='testuser2')[0]

        # Setting up Selenium
        cls.driver = webdriver.Firefox()
        super(TestUI, cls).setUpClass()

    def testLogin(self):
        self.driver.get(self.live_server_url)

        username_input = self.driver.find_element_by_id("id_username")
        username_input.send_keys('testuser2')
        password_input = self.driver.find_element_by_id("id_password")
        password_input.send_keys('testuser2')
        password_input.send_keys(Keys.ENTER)

        self.driver.implicitly_wait(2)
        # test if logged in.
        requestNewLoan = self.driver.find_element_by_id("id_requestNewLoan")
        self.assertIn("REQUEST NEW LOAN", requestNewLoan.text)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        super(TestUI, cls).tearDownClass()
