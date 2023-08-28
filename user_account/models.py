from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PlanType(models.Model):
    features = models.TextField()
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    month = models.IntegerField(default=1)
    price = models.DecimalField(default=0.0, decimal_places=2,max_digits=5)
    
    @property
    def features_list(self):
        return self.features.split(",")

class Plan(models.Model):
    type = models.OneToOneField(PlanType, on_delete=models.CASCADE, null=True)
    last_due = models.DateTimeField(auto_now_add=True)
    next_due = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="plan")
    
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    