from django import forms
from .models import Sublease, SubleasePhoto

class SubleaseForm(forms.ModelForm):
    class Meta:
        model = Sublease
        fields = 'address', 'price', 'available_from', 'available_to', 'available_text', 'description', 'cover_photo'


class SubleasePhotoForm(forms.ModelForm):
    class Meta:
        model = SubleasePhoto
        fields = ('image',)