from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

SECURITY_QUESTION_CHOICES_1 = [
    ('birth_place', 'What is the name of the town where you were born?'),
    ('sibling_name', 'What is your oldest sibling\'s middle name?'),
    ('first_school', 'What is the name of the school you attended?')
]

SECURITY_QUESTION_CHOICES_2 = [
    ('parents_city', 'In what city did your parents meet?'),
    ('first_car', 'What was the make and model of your first car?'),
    ('first_concert', 'What was the first concert you attended?')
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_question_1 = models.CharField(max_length=255, choices=SECURITY_QUESTION_CHOICES_1)
    security_answer_1 = models.CharField(max_length=255)
    security_question_2 = models.CharField(max_length=255, choices=SECURITY_QUESTION_CHOICES_2)
    security_answer_2 = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

class Asset(models.Model):
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    priority = models.CharField(max_length=50, default='Moderate')
    risk_level = models.CharField(max_length=50, default='low')
    control_measures_effectiveness = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    status_choices = [
        ('Active', 'Active'),
        ('Maintenance', 'Maintenance'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='Active')

    def __str__(self):
        return self.name
