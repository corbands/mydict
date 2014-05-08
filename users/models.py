from django.db import models
from django.contrib.auth.models import User

class EmhUser(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField()
    region = models.CharField(max_length=50)