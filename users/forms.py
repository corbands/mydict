from django import forms

class EmhUserForm(forms.Form):
	age     = forms.IntegerField(required = False)
	region  = forms.CharField(max_length = 50, required = False)
	about   = forms.CharField(required = False)

