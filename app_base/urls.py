from django.urls import path
from app_base.views import *

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register_page', register_page, name='register_page'),
    path('login_page', login_page, name='login_page'),
    path('logout_page', logout_page, name='logout_page'),

    path('profile_page', profile_page, name='profile_page'),
    path('update_profile_page', update_profile_page, name='update_profile_page'),

    path('dashboard_page', dashboard_page, name='dashboard_page'),
    path('calorie_input_page', calorie_input_page, name='calorie_input_page'),
]