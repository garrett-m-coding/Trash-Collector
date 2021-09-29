from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('confirm_charge/<int:customer_id>', views.confirm_charge, name="confirm_charge"),
    
    path('weekday_pick_up_filter/Monday', views.Monday_filter, name="Monday_filter"),
    path('weekday_pick_up_filter/Tuesday', views.Tuesday_filter, name="Tuesday_filter"),
    path('weekday_pick_up_filter/Wednesday', views.Wednesday_filter, name="Wednesday_filter"),
    path('weekday_pick_up_filter/Thursday', views.Thursday_filter, name="Thursday_filter"),
    path('weekday_pick_up_filter/Friday', views.Friday_filter, name="Friday_filter"),
]