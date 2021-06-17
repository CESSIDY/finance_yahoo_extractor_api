from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.timezone import now
from analytics.models import Companies, Analytics


class AnalyticsListSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs):
        super(AnalyticsListSerializer, self).__init__(*args, **kwargs)
        self.context_validate()
        self.last_company_analytic = self.get_last_company_analytic()

    def get_last_company_analytic(self):
        try:
            last = Analytics.objects.filter(company__symbol=self.context['symbol']).latest('date')
            return last
        except ObjectDoesNotExist:
            return None

    def context_validate(self):
        if 'symbol' not in self.context:
            raise serializers.ValidationError({"symbol": "context don't have a symbol field"})
        return True

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        company, _ = Companies.objects.get_or_create(
            symbol=self.context['symbol'],
        )
        analytics = list()
        for item in validated_data:
            if not self.last_company_analytic:
                new_analytic = Analytics(company=company,
                                         date=item['date'],
                                         open=item['open'],
                                         high=item['high'],
                                         low=item['low'],
                                         adj=item['adj'],
                                         close=item['close'],
                                         volume=item['volume'],
                                         )
                analytics.append(new_analytic)
            elif self.last_company_analytic.date < item['date']:
                new_analytic = Analytics(company=company,
                                         date=item['date'],
                                         open=item['open'],
                                         high=item['high'],
                                         low=item['low'],
                                         adj=item['adj'],
                                         close=item['close'],
                                         volume=item['volume'],
                                         )
                analytics.append(new_analytic)
        return Analytics.objects.bulk_create(analytics)


class AnalyticsSerializer(serializers.Serializer):
    date = serializers.DateField()
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    adj = serializers.FloatField()
    close = serializers.FloatField()
    volume = serializers.FloatField()

    class Meta:
        list_serializer_class = AnalyticsListSerializer

    def __init__(self, *args, **kwargs):
        super(AnalyticsSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        attrs = super(AnalyticsSerializer, self).validate(attrs)
        if attrs:
            return attrs
        raise serializers.ValidationError({"attrs": "attrs are empty"})

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AnalyticsModelSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source='company.symbol')

    class Meta:
        model = Analytics
        fields = ('symbol', 'date', 'open', 'high', 'low', 'adj', 'close', 'volume')
