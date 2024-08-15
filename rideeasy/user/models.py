from django.db import models
from django.contrib.auth.models import User
from seller.models import Car

# Create your models here.
#If a user or car is deleted, the corresponding cart items are also deleted, maintaining database integrity.
class Detail(models.Model):
   uid=models.ForeignKey(User, on_delete=models.CASCADE,db_column="uid")
   pid=models.ForeignKey(Car, on_delete=models.CASCADE,db_column="pid")
   quantity=models.IntegerField(default=1)
