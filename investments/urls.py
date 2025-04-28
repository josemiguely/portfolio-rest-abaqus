from django.urls import path
from investments.views import PortfolioMetricsView

app_name = 'investments'

urlpatterns = [
    path('portfolio-metrics/', PortfolioMetricsView.as_view(), name='portfolio-metrics'),
]