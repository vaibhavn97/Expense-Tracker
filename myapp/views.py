from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Expense
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
import datetime

# Create your views here.
def home(request):
    return render(request, 'myapp/landing.html')

class ExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = "myapp/dashboard.html"
    context_object_name = 'expenses'
    fields = ['name', 'category', 'amount']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["expenses"] = self.model.objects.filter(user=self.request.user)
        year_parms = datetime.datetime.today() - datetime.timedelta(days=365)
        month_parms = datetime.datetime.today() - datetime.timedelta(days=30)
        seven_parms = datetime.datetime.today() - datetime.timedelta(days=7)
        year = self.model.objects.filter(user=self.request.user, date__gt=year_parms).aggregate(Sum('amount'))
        month = self.model.objects.filter(user=self.request.user, date__gt=month_parms).aggregate(Sum('amount'))
        seven = self.model.objects.filter(user=self.request.user, date__gt=seven_parms).aggregate(Sum('amount'))
        context['date_sum'] = {
            'year':year['amount__sum'],
            'month': month['amount__sum'],
            'seven': seven['amount__sum']
        }
        context['daily_sum'] = self.model.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
        context['category_sum'] = self.model.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
        
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExpenseEditView(LoginRequiredMixin, UpdateView):
    model = Expense    
    template_name = "myapp/expenseEdit.html"
    fields = ['name', 'category', 'amount']

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'myapp/expenseDelete.html'
    success_url = '/dashboard'

