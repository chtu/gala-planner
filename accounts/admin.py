from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, UserManager

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

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'password', 'is_active', 'is_admin')

	def clean_password(self):
		return self.initial["password"]

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'last_name', 'first_name')
	list_filter = ('is_admin','is_planner', 'email')
	fieldsets = (
		(None, {'fields': ('email', 'password',)}),
		('Personal info', {'fields': ('first_name', 'last_name',)}),
		('Permissions', {'fields': ('is_admin',)}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
		}),
	)

	search_fields = ('email', 'last_name', 'first_name')
	ordering = ('email', 'last_name', 'first_name')
	filter_horizontal = ()

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)