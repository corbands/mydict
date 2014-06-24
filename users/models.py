from django.db import models
from django.contrib.auth.models import User

class EmhUser(models.Model):
	user    = models.OneToOneField(User)
	age     = models.IntegerField(null = True)
	region  = models.CharField(max_length = 50, null = True)
	about   = models.TextField(null = True, default = '')