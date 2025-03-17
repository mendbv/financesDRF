import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    date = django_filters.DateFromToRangeFilter(field_name="date")

    class Meta:
        model = Transaction
        fields = ['category', 'type', 'min_amount', 'max_amount', 'date']
