from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.ExpenseView.as_view(), name='dash'),
    path('expense/<int:pk>', views.ExpenseEditView.as_view(), name='expense-edit'),
    path('expense/remove/<int:pk>', views.ExpenseDeleteView.as_view(), name='expense-remove'),

]