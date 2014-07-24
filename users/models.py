from django.db import models
from django.contrib.auth.models import User

class EmhUser(models.Model):
	user    = models.OneToOneField(User)
	region  = models.CharField(max_length = 50, null = True, blank = True)
	about   = models.TextField(null = True, default = '', blank = True)
	avatar  = models.ImageField(upload_to = 'avatars', blank = True, null = True)