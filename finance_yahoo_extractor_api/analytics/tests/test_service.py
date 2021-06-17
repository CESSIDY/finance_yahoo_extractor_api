from django.test import TestCase
from django.urls import reverse
from analytics.models import Companies
from analytics.service import YahooAnalyticsService


class ApiTestCase(TestCase):
    def setUp(self):
        self.service = YahooAnalyticsService()
        self.analytics_fields = ['date', 'open', 'high', 'low', 'adj', 'close', 'volume']

    def test_get_analytics_by_symbol(self):
        service = YahooAnalyticsService()
        symbol = 'DKNG'
        analytics_data = service.get_analytics_by_symbol(symbol)

        self.assertTrue(analytics_data)
        # take first element and check it
        self.assertTrue(list(analytics_data[0].keys()) == self.analytics_fields)

    def test_get_analytics_for_all_saving_companies(self):
        service = YahooAnalyticsService()

        url = reverse('analytics:update_default')
        _ = self.client.put(url)

        companies_symbol = Companies.objects.values_list('symbol', flat=True)

        updating_symbols = list()

        for symbol, analytics_data in service.get_analytics_for_all_saving_companies():
            updating_symbols.append(symbol)

        self.assertEquals(updating_symbols, list(companies_symbol))

    def test_get_analytics_for_default_companies(self):
        service = YahooAnalyticsService()

        url = reverse('analytics:update_default')
        _ = self.client.put(url)

        companies_symbol = Companies.objects.values_list('symbol', flat=True)

        updating_symbols = list()

        for symbol, analytics_data in service.get_analytics_for_default_companies():
            updating_symbols.append(symbol)

        self.assertEquals(updating_symbols, list(companies_symbol))
