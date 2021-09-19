from django.urls import path

from employees import views


urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employees_list'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
]