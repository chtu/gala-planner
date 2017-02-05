from django import forms

from tablesetter.models import Table


class UserCheckForm(forms.Form):
	email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(attrs={'placeholder':"Sponsor's email"}))

	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email.lower()

class InviteForm(forms.Form):
	email = forms.EmailField(required=True, widget=forms.HiddenInput())
	table_size = forms.IntegerField(required=True)

	def clean_num_tables(self):
		num_tables = self.cleaned_data.get('num_tables')

		if num_tables > 0 and num_tables < 99:
			return num_tables
		else:
			raise forms.ValidationError("That's too many tables!")

	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email.lower()

class TableForm(forms.ModelForm):
	class Meta:
		model = Table
		fields = ['table_size']
		widgets = {
			'table_size': forms.TextInput(attrs={'placeholder':'Number of Seats', 'required':True}),
		}

	def clean_table_size(self):
		table_size = self.cleaned_data.get('table_size')
		if table_size <= 0:
			raise forms.ValidationError('The table size cannot be zero or a negative number.')
		elif table_size > 99:
			raise forms.ValidationError('The table size cannot be too large.')
		else:
			return table_size