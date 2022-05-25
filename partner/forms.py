
from django import forms

class companyform(forms.Form):
	company = forms.IntegerField(label = 'Business Code')

class branchform(forms.Form):
	branch = forms.IntegerField(label = 'Branch Code')