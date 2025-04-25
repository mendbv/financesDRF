from rest_framework.viewsets import ModelViewSet
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
import csv

from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer
from .filters import TransactionFilter

# Словарь с описаниями операций для Swagger
SWAGGER_OPERATIONS = {
    'list': {
        'description': "Возвращает список всех {entity} пользователя.",
        'summary': "Список {entity}",
    },
    'create': {
        'description': "Создаёт новую {entity}.",
        'summary': "Создание {entity}",
    },
    'retrieve': {
        'description': "Возвращает конкретную {entity}.",
        'summary': "Детали {entity}",
    },
    'update': {
        'description': "Обновляет {entity}.",
        'summary': "Обновление {entity}",
    },
    'partial_update': {
        'description': "Частично обновляет {entity}.",
        'summary': "Частичное обновление {entity}",
    },
    'destroy': {
        'description': "Удаляет {entity}.",
        'summary': "Удаление {entity}",
    }
}

def apply_swagger_decorators(entity_name):
    """Динамически создаёт декораторы для методов ViewSet."""
    def decorator(cls):
        for method, config in SWAGGER_OPERATIONS.items():
            description = config['description'].format(entity=entity_name)
            summary = config['summary'].format(entity=entity_name)
            cls = method_decorator(
                name=method,
                decorator=swagger_auto_schema(operation_description=description, operation_summary=summary)
            )(cls)
        return cls
    return decorator

class BaseUserViewSet(ModelViewSet):
    """Базовый класс для ViewSet с фильтрацией по пользователю."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

@apply_swagger_decorators('категорий')
class CategoryViewSet(BaseUserViewSet):
    serializer_class = CategorySerializer
    model = Category

@apply_swagger_decorators('транзакций')
class TransactionViewSet(BaseUserViewSet):
    serializer_class = TransactionSerializer
    model = Transaction
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Возвращает аналитику по доходам и расходам пользователя.",
    operation_summary="Аналитика",
))
class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        category_summary = transactions.values('category__name').annotate(total=Sum('amount'))

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "category_summary": list(category_summary),
        })

@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Экспортирует транзакции пользователя в CSV файл.",
    operation_summary="Экспорт CSV",
))
class ExportCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        response = HttpResponse(content_type='text/csv', headers={
            'Content-Disposition': 'attachment; filename="transactions.csv"'
        })

        writer = csv.writer(response)
        writer.writerow(['Дата', 'Категория', 'Сумма', 'Тип'])
        for t in transactions:
            writer.writerow([t.date, t.category.name, t.amount, t.type])

        return response