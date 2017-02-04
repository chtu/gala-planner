from django import forms


class UserCheckForm(forms.Form):
	email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(attrs={'placeholder':"Sponsor's email"}))

	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email.lower()

class InviteForm(forms.Form):
	email = forms.EmailField(required=True, widget=forms.HiddenInput())
	num_tables = forms.IntegerField(required=True)

	def clean_num_tables(self):
		num_tables = self.cleaned_data.get('num_tables')

		if num_tables > 0 and num_tables < 99:
			return num_tables
		else:
			raise forms.ValidationError("That's too many tables!")

	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email.lower()