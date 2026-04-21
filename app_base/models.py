from django.db import models
from django.contrib.auth.models import User

# Name, Age, Gender, Height, Weight bmr total_consumed_today
class ProfileModel(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)

    GENDER = [
        ('Male', 'Male'), 
        ('Female', 'Female'),
    ]
    name = models.CharField(max_length=255, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(choices= GENDER, max_length=50, null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    bmr = models.FloatField(null=True)
    total_consumed_today = models.FloatField(null=True)
    goal_weight = models.FloatField(null=True)
    bmi = models.FloatField(null=True)

    def __str__(self):
        return self.name

class CalorieHistoryModel(models.Model):
    user = models.ForeignKey(User, related_name='track_calorie', on_delete=models.CASCADE, null=True)

    total_protein_today = models.FloatField(null=True, default=0.0)
    total_carbs_today = models.FloatField(null=True, default=0.0)
    total_fat_today = models.FloatField(null=True, default=0.0)
    total_consumed_today = models.FloatField(default=0.0, null=True)

    date = models.DateField(auto_now_add=True, null=True)
    
# (Item name, Calorie consumed)
class CalorieInputModel(models.Model):
    user = models.ForeignKey(User, related_name='user_calorie_inputs', on_delete=models.CASCADE, null=True)
    history = models.ForeignKey(CalorieHistoryModel, related_name='history_calorie_inputs', on_delete=models.CASCADE, null=True)

    item_name = models.CharField(max_length=255, null=True)
    protein = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    fat = models.FloatField(null=True)

    calorie_consumed = models.FloatField(null=True) # proitein + carbs + fat
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.item_name





