from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

cat = (
    ('Food', 'Food'),
    ('Other', 'Other'),
    ('Education', 'Education'),
    ('Office', 'Office'),
    ('Personal', 'Personal')
)

class Expense(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=40, choices=cat)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('dash')

    def __str__(self):
        return f"{self.name} by {self.user}"