from django.contrib import admin
from django.urls import path
from analytics.views import UpdateAnalyticsView, UpdateDefaultAnalyticsView, GetAnalyticsView

urlpatterns = [
    # update analytics for some company
    path('api/update/symbol=<symbol>', UpdateAnalyticsView.as_view(), name='update_by_symbol_analytics'),
    # update analytics from the list of default companies
    path('api/update/default', UpdateDefaultAnalyticsView.as_view(), name='update_default_analytics'),
    # update analytics for all companies in database
    path('api/update/', UpdateAnalyticsView.as_view(), name='update_all_analytics'),
    # get analytics from database for some company
    path('api/get/symbol=<symbol>', GetAnalyticsView.as_view(), name='get_by_symbol_analytics'),
]
