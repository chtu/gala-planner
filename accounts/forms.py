from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match")
		return password2

	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email.lower()

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.first_name = user.first_name.upper()
		user.last_name = user.last_name.upper()

		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserSigninForm(forms.Form):
	email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'placeholder':'E-mail'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email.lower()