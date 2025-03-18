from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')


    def __str__(self):
        return self.name

class Transaction(models.Model):
    TYPE_CHOICES = (('income', 'Доход'), ('expense', 'Расход'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)

    def __str__(self):
        return f"{self.type} - {self.amount} ({self.category})"
