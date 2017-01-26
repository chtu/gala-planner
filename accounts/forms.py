from django import forms
from .models import User

class PlannerSignupForm(forms.Form):
	email = forms.EmailField(label='email',
		widget=forms.TextInput(attrs={
			"placeholder": "Email",
			}))

	first_name = forms.CharField(label='first name',
		widget=forms.TextInput(attrs={
			"placeholder": "First Name",
			}))

	last_name = forms.CharField(label='last name',
		widget=forms.TextInput(attrs={
			"placeholder": "Last Name",
			}))

	password_one = forms.CharField(label="password1",
		widget=forms.PasswordInput(attrs={
			"placeholder":"New Password",
			}))
	
	password_two = forms.CharField(label='password2',
		widget=forms.PasswordInput(attrs={
			"placeholder":"Retype your password",
			}))