from django import forms
from seller.models import Car

class ImageForm(forms.ModelForm):
   class Meta:
      model=Car
      fields=['image']