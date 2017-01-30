from django import forms

from .models import Gala



class GalaForm(forms.ModelForm):
	class Meta:
		model = Gala
		fields = ['gala_name', 'gala_date', 'gala_time']

class GalaUpdateForm(forms.Form):
	gala_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'placeholder':'Update name'}))
	gala_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder':'update date'}))
	gala_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'placeholder':'update time'}))