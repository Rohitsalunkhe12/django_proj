from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    name = models.CharField(max_length=50)
    rent = models.FloatField()
    owner = models.CharField(max_length=50, default='default_owner')  # Provide a default value
    model = models.CharField(max_length=50, default='default_model')  # Provide a default value
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    quantity = models.IntegerField()
    is_active = models.BooleanField()
    image = models.ImageField(upload_to='image/')
    sid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="sid")
