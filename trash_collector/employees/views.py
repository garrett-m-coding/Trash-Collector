from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from .models import Employee
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
import calendar

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    

    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        today_weekday = calendar.day_name[today.weekday()]
        
        same_zip_code = Customer.objects.filter(zip_code = logged_in_employee.zip_code)

        same_pickup_day = same_zip_code.filter(weekly_pickup = today_weekday)

        one_time = same_zip_code.filter(one_time_pickup = today)

        status_weekly = same_pickup_day.exclude(suspend_start__lt = today) and same_pickup_day.exclude(suspend_end__gt = today)

        status_one_time = one_time.exclude(suspend_start__lt = today) and one_time.exclude(suspend_end__gt = today)

        #   Attempt to create a method to clean up/ reduce code for filtering
        
        # def filter_customers(list_of_customers, property, comparison):
        #     new_list = list_of_customers.filter(property = comparison)
        #     return new_list

        # same_zip_code = filter_customers(Customer.objects, zip_code, )

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'status_weekly': status_weekly,
            'status_one_time': status_one_time
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

@login_required
def confirm_charge(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    customer_to_update = Customer.objects.get(id=customer_id)
    today = date.today()
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        customer_to_update.date_of_last_pickup = today
        customer_to_update.balance += 20
        customer_to_update.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'customer_to_update': customer_to_update
        }
        return render(request, 'employees/confirm_charge.html', context)
        # ?use filtered customer list for customer?
        # take the client status weekly and one time clients->
        # confirm client's trash picked up
        # update client's latest pickup date
        # charge trash pickup client $20
        