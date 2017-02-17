from django import forms

from tablesetter.models import Table


class UserCheckForm(forms.Form):
	email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(attrs={'placeholder':"Sponsor's email"}))

	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email.lower()