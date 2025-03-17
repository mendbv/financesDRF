from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, TransactionViewSet, AnalyticsView, ExportCSVView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)), 
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('export/csv/', ExportCSVView.as_view(), name='export_csv'),
]