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

@login_required
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

        status_weekly = same_pickup_day.exclude(suspend_start__lt = today) | same_pickup_day.exclude(suspend_end__gt = today)
        
        status_one_time = one_time.exclude(suspend_start__lt = today) | one_time.exclude(suspend_end__gt = today)

        incomplete_pick_up = status_weekly.exclude(date_of_last_pickup = today) | status_one_time.exclude(date_of_last_pickup = today)

        completed_pick_up = status_weekly.filter(date_of_last_pickup = today) | status_one_time.filter(date_of_last_pickup = today)

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'incomplete_pick_up':incomplete_pick_up,
            'completed_pick_up': completed_pick_up
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

@login_required
def Monday_filter(request):
    Customer = apps.get_model('customers.Customer')
    weekday_filter = Customer.objects.filter(weekly_pickup = "Monday")
    print(weekday_filter)
    context = {
        'weekday_filter': weekday_filter,
        'weekday': 'Monday',
    }
    return render(request, 'employees/weekday_pick_up_filter.html', context)

@login_required
def Tuesday_filter(request):
    Customer = apps.get_model('customers.Customer')
    weekday_filter = Customer.objects.filter(weekly_pickup = "Tuesday")
    context = {
        'weekday_filter': weekday_filter,
        'weekday': 'Tuesday',
    }
    return render(request, 'employees/weekday_pick_up_filter.html', context)

@login_required
def Wednesday_filter(request):
    Customer = apps.get_model('customers.Customer')
    weekday_filter = Customer.objects.filter(weekly_pickup = "Wednesday")
    context = {
        'weekday_filter': weekday_filter,
        'weekday': 'Wednesday',
    }
    return render(request, 'employees/weekday_pick_up_filter.html', context)

@login_required
def Thursday_filter(request):
    Customer = apps.get_model('customers.Customer')
    weekday_filter = Customer.objects.filter(weekly_pickup = "Thursday")
    context = {
        'weekday_filter': weekday_filter,
        'weekday': 'Thursday',
    }
    return render(request, 'employees/weekday_pick_up_filter.html', context)   

@login_required
def Friday_filter(request):
    Customer = apps.get_model('customers.Customer')
    weekday_filter = Customer.objects.filter(weekly_pickup = "Friday")
    context = {
        'weekday_filter': weekday_filter,
        'weekday': 'Friday',
    }
    return render(request, 'employees/weekday_pick_up_filter.html', context)             
