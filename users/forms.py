from django import forms

class EmhUserForm(forms.Form):
	first_name = forms.CharField(required = False)
	last_name  = forms.CharField(required = False)
	region     = forms.CharField(required = False)
	about      = forms.CharField(required = False)


class EmhUserRegisterForm(EmhUserForm):
	username  = forms.CharField()
	password  = forms.CharField()
	password2 = forms.CharField()
