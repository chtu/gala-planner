from django import forms

from tablesetter.models import Table



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