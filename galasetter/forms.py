from django import forms

from .models import Gala, MealChoice



class GalaForm(forms.ModelForm):
	class Meta:
		model = Gala
		fields = ['gala_name', 'gala_date', 'gala_time']

class GalaUpdateForm(forms.Form):
	gala_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'placeholder':'Update name'}))
	gala_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder':'update date'}))
	gala_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'placeholder':'update time'}))

class AddMealChoiceForm(forms.ModelForm):
	class Meta:
		model = MealChoice
		fields = ['choice_text', 'choice_desc']

class EditMealChoiceForm(forms.Form):
	choice_text = forms.CharField(required=False, max_length=200)
	choice_desc = forms.CharField(required=False, max_length=500)