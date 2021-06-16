from rest_framework import generics, status
from rest_framework.response import Response
from analytics.models import Analytics, Companies
from analytics.service import YahooAnalyticsService, YahooAnalyticsException
from analytics.serializers import AnalyticsSerializer, AnalyticsModelSerializer


class UpdateDefaultAnalyticsView(generics.GenericAPIView):

    @staticmethod
    def put(request):
        service = YahooAnalyticsService()
        for symbol, analytics_data in service.get_analytics_for_default_companies():
            serializer = AnalyticsSerializer(data=analytics_data, context={'symbol': symbol}, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class UpdateAnalyticsView(generics.GenericAPIView):

    @staticmethod
    def put(request, symbol=None):
        service = YahooAnalyticsService()

        # update analytics for some company by their symbol
        if symbol:
            try:
                analytics_data = service.get_analytics_by_symbol(symbol)
                serializer = AnalyticsSerializer(data=analytics_data, context={'symbol': symbol}, many=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except YahooAnalyticsException:
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # update analytics for companies in database
        for symbol, analytics_data in service.get_analytics_for_all_saving_companies():
            serializer = AnalyticsSerializer(data=analytics_data, context={'symbol': symbol}, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class GetAnalyticsView(generics.ListCreateAPIView):
    serializer_class = AnalyticsModelSerializer

    def get_queryset(self):
        if 'symbol' in self.kwargs:
            queryset = Analytics.objects.filter(company__symbol=self.kwargs['symbol'])
            return queryset
        return None
