from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from app_base.forms import *
from app_base.models import *
from datetime import date
from django.db.models import Sum

def home_page(request):
    return render(request, 'home_page.html')

def register_page(request):

    if request.method == "POST":
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_page')
    
    form = RegisterForm()
    context = {
        'form': form,
        'heading': 'Register User',
        'action': 'Register'
    }
    return render(request, 'base-auth.html', context)

def login_page(request):

    if request.method == "POST":
        form_data = LoginForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            login(request, user)
            return redirect('profile_page')
    form = LoginForm()
    context = {
        'form': form,
        'heading': 'Login User',
        'action': 'Login'
    }
    return render(request, 'base-auth.html', context)

@login_required
def profile_page(request):
    try:
        profile = request.user.profile
    except:
        profile = None
    
    if profile:
        total_calories_today = profile.total_consumed_today
        calorie_needed = profile.bmr-profile.total_consumed_today

    else:
        total_calories_today = 0
        calorie_needed = 0

    context = {
        'total_calories_today': total_calories_today,
        'calorie_needed': calorie_needed
    }
    return render(request, 'profile_page.html', context)

@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def update_profile_page(request):

    try:
        profile = request.user.profile
    except ProfileModel.DoesNotExist:
        profile = None

    if request.method == "POST":
        form_data = ProfileForm(request.POST, instance = profile)
        if form_data.is_valid():
            form_data = form_data.save(commit=False)
            form_data.user = request.user
            if not form_data.total_consumed_today:
                form_data.total_consumed_today = 0
            w = form_data.weight or 0
            h = form_data.height or 0
            a = form_data.age or 0
            # for male 66.47+(13.75 x weight in kg) + (5.003 x height in cm) - (6.755 x age in years)
            # for female 655.1+(9.563 x weight in kg)+(1.850 x height in cm) - (4.676 x age in years) 
            if form_data.gender == 'male':
                form_data.bmr = 66.47+(13.75*w)+(50.003*h)-(6.755*a)
            else:
                form_data.bmr = 655.1+(9.563*w)+(1.850*h)-(4.676*a)
            # BMI = weight (kg) ÷ height (m²). 
            form_data.bmi = (w*10000)/(h**2)
            form_data.save()
            return redirect('profile_page')
    
    form = ProfileForm(instance = profile)
    context = {
        'form': form,
        'heading': 'Profile Info',
        'action': 'Update Profile'
    }
    return render(request, 'base-form.html', context)

@login_required
def dashboard_page(request):
    # total = total calorie consumed today
    consumptions = CalorieInputModel.objects.filter(user = request.user, date=date.today())
    # total = consumptions.aggregate(total = Sum('calorie_consumed'))['total'] or 0
    
    # profile = ProfileModel.objects.get(user=request.user)
    # profile.total_consumed_today = total
    # profile.save()

    # CalorieInputModel.objects.filter(user=request.user, date=date.today()).update(
    #     total_consumed_today = total
    # )

    # ----In your view
    try:
        profile = request.user.profile
    except:
        profile = None
    
    if profile:
        bmr = profile.bmr
        total_cals = profile.total_consumed_today  # already have this

    ring_percent = min(round((total_cals / bmr) * 100), 100) if bmr else 0
    ring_offset = round(471 - (471 * ring_percent / 100))  # 471 = 2π×75 (circle circumference)

    try:
        todays_stat = CalorieHistoryModel.objects.get(
            user = request.user,
            date = date.today()
        )
    except:
        todays_stat = None
    
    if  todays_stat:
        total_protein = todays_stat.total_protein_today
        total_carbs = todays_stat.total_carbs_today
        total_fat = todays_stat.total_fat_today
    else:
        total_protein = 0
        total_carbs = 0
        total_fat = 0

    context = {
        'consumptions': consumptions,
        'total': total_cals,
        'ring_percent': ring_percent,
        'ring_offset': ring_offset,
        'total_protein': total_protein,   # sum of protein today
        'total_carbs': total_carbs,     # sum of carbs today
        'total_fat': total_fat,       # sum of fat today
        'protein_goal': ...,    # e.g. from profile
        'carb_goal': ...,
        'fat_goal': ...,
    }
    return render(request, 'dashboard_page.html', context)


@login_required
def calorie_input_page(request):

    if request.method == "POST":
        form_data = CalorieInputForm(request.POST)
        if form_data.is_valid():
            form_data = form_data.save(commit=False)
            form_data.user = request.user
            p = form_data.protein
            c = form_data.carbs
            f = form_data.fat
            form_data.calorie_consumed = p + c + f
            try:
                todays_history = CalorieHistoryModel.objects.get(
                    user = request.user,
                    date = date.today()
                )
            except:
                todays_history = CalorieHistoryModel.objects.create(
                    user = request.user
                )
            form_data.history = todays_history
            form_data.save()
            #-----Update history
            todays_history.total_protein_today += p
            todays_history.total_carbs_today += c
            todays_history.total_fat_today += f
            todays_history.total_consumed_today += form_data.calorie_consumed
            todays_history.save()
            #-----Update profile
            request.user.profile.total_consumed_today = todays_history.total_consumed_today
            request.user.profile.save()
            return redirect('dashboard_page')
    form = CalorieInputForm()
    context = {
        'form': form,
        'heading': 'Calorie Input',
        'action': 'calculate'
    }
    return render(request, 'base-form.html', context)