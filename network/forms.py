from django import forms
from .models import User

class ProfilePicForm(forms.Form):
    profile_image = forms.ImageField(label="", help_text="", widget=forms.FileInput(attrs={
        'id':'file',
        'name': 'profile-image',
        'type': 'file'
        }))