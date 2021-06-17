from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient
from analytics.service import YahooAnalyticsService


class ApiTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_url_updating_by_symbol(self):
        symbol = 'DKNG'
        url = reverse('analytics:update_by_symbol', kwargs={'symbol': symbol})
        response = self.client.put(url)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['updated'], symbol)

    def test_url_updating_all(self):
        symbols = ['DKNG', "CLDR", "RUN"]
        # adding new data in database before testing
        for symbol in symbols:
            url = reverse('analytics:update_by_symbol', kwargs={'symbol': symbol})
            _ = self.client.put(url)

        url = reverse('analytics:update_all')
        response = self.client.put(url)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['updated'], symbols)

    def test_url_updating_default(self):
        service = YahooAnalyticsService()

        url = reverse('analytics:update_default')
        response = self.client.put(url)

        self.assertEquals(response.status_code, 201)

        # it is possible that the data for some company were not found on the site, such as PVTL
        for symbol in response.data['updated']:
            self.assertIn(symbol, service.default_symbols)

    def test_url_get_by_symbol(self):
        symbol = 'DKNG'
        url = reverse('analytics:get_by_symbol', kwargs={'symbol': symbol})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
