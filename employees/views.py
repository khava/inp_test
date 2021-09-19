from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from employees.models import Employee

class EmployeeListView(View):
    def get(self, request):
        context = {
            'employees': Employee.objects.all()
        }
        
        return render(request, 'employees/list_employees.html', context)


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employees/detail_employee.html'
    context_object_name = 'employee'
