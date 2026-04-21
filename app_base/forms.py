from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app_base.models import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for x in self.fields.values():
            x.widget.attrs.update({'class': 'form-control'})

class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for x in self.fields.values():
            x.widget.attrs.update({'class': 'form-control'})

# Name, Age, Gender, Height, Weight bmr total_consumed_today
class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = [
            'name',
            'age',
            'gender',
            'height',
            'weight',
            'goal_weight',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for x in self.fields.values():
            x.widget.attrs.update({'class': 'form-control'})

# (Item name, Calorie consumed) date
class CalorieInputForm(forms.ModelForm):
    class Meta:
        model = CalorieInputModel
        fields = [
            'item_name',
            'protein',
            'carbs',
            'fat'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for x in self.fields.values():
            x.widget.attrs.update({'class': 'form-control'})