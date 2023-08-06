from NEMO.models import User
from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from NEMO_reports.tests.test_utilities import test_response_is_landing_page
from NEMO_reports.views.reporting import billing_installed


class TestReports(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(
            username="test_user", first_name="Testy", last_name="McTester", badge_number=1
        )
        self.accounting, created = User.objects.get_or_create(
            username="test_accounting",
            first_name="Testy",
            last_name="McTester",
            badge_number=2,
            is_accounting_officer=True,
        )

    def test_master_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reporting"), follow=True)
        test_response_is_landing_page(self, response)
        self.client.force_login(self.accounting)
        response = self.client.get(reverse("reporting"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_unique_users_report(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reporting_unique_users"), follow=True)
        test_response_is_landing_page(self, response)
        self.client.force_login(self.accounting)
        response = self.client.get(reverse("reporting_unique_users"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_unique_user_project_report(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reporting_unique_user_project"), follow=True)
        test_response_is_landing_page(self, response)
        self.client.force_login(self.accounting)
        response = self.client.get(reverse("reporting_unique_user_project"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_unique_user_account_report(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reporting_unique_user_account"), follow=True)
        test_response_is_landing_page(self, response)
        self.client.force_login(self.accounting)
        response = self.client.get(reverse("reporting_unique_user_account"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_invoice_charges_report(self):
        if billing_installed():
            self.client.force_login(self.user)
            response = self.client.get(reverse("reporting_invoice_charges"), follow=True)
            test_response_is_landing_page(self, response)
            self.client.force_login(self.accounting)
            response = self.client.get(reverse("reporting_invoice_charges"), follow=True)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertRaises(NoReverseMatch, reverse, "reporting_invoice_charges")

    def test_invoice_item_charges_report(self):
        if billing_installed():
            self.client.force_login(self.user)
            response = self.client.get(reverse("reporting_invoice_item_charges"), follow=True)
            test_response_is_landing_page(self, response)
            self.client.force_login(self.accounting)
            response = self.client.get(reverse("reporting_invoice_item_charges"), follow=True)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertRaises(NoReverseMatch, reverse, "reporting_invoice_item_charges")
