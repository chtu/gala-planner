from django import forms


class UserCheckForm(forms.Form):
	email = forms.CharField(max_length=150, required=True)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email.lower()