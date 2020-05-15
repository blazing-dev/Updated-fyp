from django import forms
from .models import Employees, VisitLog, Visitors
from django.core.validators import validate_email

class Employee_form(forms.ModelForm):
   class Meta:
      model = Employees
      fields = ['emp_id', 'emp_name', 'emp_mobile', 'emp_address', 'emp_designation', 'emp_photo_path']

class Visitors_form(forms.ModelForm):
   vis_id = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Visitor ID e.g, 001, 112 etc'}), required=True, max_length=50)
   vis_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Visitor name'}))
   vis_email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Visitor email'}))
   vis_type = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Visitor type'}), required=True, max_length=50)

   class Meta:
      model = Visitors
      fields = ['vis_id', 'vis_name', 'vis_type', 'vis_photo_path', 'vis_photo_file']

   def clean_vis_id(self):
      id = self.cleaned_data['vis_id']
      try:
         match = Visitors.objects.get(vis_id = id)
      except:
         return self.cleaned_data['vis_id']
      raise forms.ValidationError("Visitor ID already exist")

   def clean_vis_email(self):
      email = self.cleaned_data['vis_email']
      try:
         match = validate_email(email)
      except:
         return forms.ValidationError("Invalid Email address")
      return email