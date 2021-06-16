from django.contrib import admin
from analytics.models import Companies, Analytics


class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('symbol',)


class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date', 'open',)

    @staticmethod
    def symbol(instance):
        return instance.company.symbol


admin.site.register(Companies, CompaniesAdmin)
admin.site.register(Analytics, AnalyticsAdmin)
