import time
from typing import Generator
import requests
from finance_yahoo_extractor_api.settings import FINANCE_YAHOO_URL
from analytics.models import Companies
from datetime import datetime


class YahooAnalyticsException(Exception):
    def __init__(self, symbol, message="Data extracting exception"):
        self.symbol = symbol
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.symbol} -> {self.message}'


class YahooAnalyticsService:
    def __init__(self):
        self.default_symbols = ["PD", "ZUO", "PINS", "ZM", "PVTL", "DOCU", "CLDR", "RUN"]

    @staticmethod
    def _format_response_to_analytic_data(content):
        result = []

        def remove_double_sided_marks(data_str):
            return data_str[1:-2]

        def split_by_new_line(data_str):
            return data_str.split("\\n")

        def remove_header(data_str):
            return data_str[1:]

        content = str(content)
        content = remove_double_sided_marks(content)
        content = split_by_new_line(content)
        content = remove_header(content)

        for line in content:
            values = line.split(",")
            result.append({'date': datetime.strptime(values[0], '%Y-%m-%d').date(),
                           'open': float(values[1]),
                           'high': float(values[2]),
                           'low': float(values[3]),
                           'adj': float(values[4]),
                           'close': float(values[5]),
                           'volume': float(values[6])})
        return result

    # returns a list of analytics from a site by a company symbol
    def get_analytics_by_symbol(self, symbol: str) -> list:
        url = FINANCE_YAHOO_URL.format(symbol=symbol, current_unix_date=int(time.time()))

        try:
            response = requests.get(url, allow_redirects=True)
        except requests.RequestException:
            raise YahooAnalyticsException(symbol)

        if response.status_code == 200:
            return self._format_response_to_analytic_data(response.content)
        raise YahooAnalyticsException(symbol)

    # returns a Generator of analytics from a site for all companies in database
    def get_analytics_for_all_saving_companies(self) -> Generator[list, None, None]:
        for company in Companies.objects.all():
            try:
                result = self.get_analytics_by_symbol(company.symbol)
            except YahooAnalyticsException:
                continue
            yield company.symbol, result

    # returns a Generator of analytics from a site for all default companies
    def get_analytics_for_default_companies(self) -> Generator[tuple, None, None]:
        for symbol in self.default_symbols:
            try:
                result = self.get_analytics_by_symbol(symbol)
            except YahooAnalyticsException:
                continue
            yield symbol, result
