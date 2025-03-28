from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Sum
from django.http import HttpResponse
import csv

from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer
from .filters import TransactionFilter

@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Возвращает список всех категорий пользователя.",
    operation_summary="Список категорий",
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создаёт новую категорию.",
    operation_summary="Создание категории",
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Возвращает конкретную категорию.",
    operation_summary="Детали категории",
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Обновляет категорию.",
    operation_summary="Обновление категории",
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Частично обновляет категорию.",
    operation_summary="Частичное обновление категории",
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удаляет категорию.",
    operation_summary="Удаление категории",
))
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Возвращает список всех транзакций пользователя.",
    operation_summary="Список транзакций",
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создаёт новую транзакцию.",
    operation_summary="Создание транзакции",
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Возвращает конкретную транзакцию.",
    operation_summary="Детали транзакции",
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Обновляет транзакцию.",
    operation_summary="Обновление транзакции",
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Частично обновляет транзакцию.",
    operation_summary="Частичное обновление транзакции",
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удаляет транзакцию.",
    operation_summary="Удаление транзакции",
))
class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Возвращает аналитику по доходам и расходам пользователя.",
    operation_summary="Аналитика",
))
class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)

        total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

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
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Дата', 'Категория', 'Сумма', 'Тип'])
        for transaction in transactions:
            writer.writerow([transaction.date, transaction.category.name, transaction.amount, transaction.type])

        return response
