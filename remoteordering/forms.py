from django import forms
class NameForm(forms.Form):
	your_name = forms.CharField(label = "Your_name",max_length  = 100)
	age = forms.IntegerField(label = "Your_age")




