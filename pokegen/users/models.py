from django import forms
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='empty_profile.png', upload_to='profile_pics')
    desc = models.TextField(max_length=1000, default="")

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if (self.image and 
        self.image.name and 
        hasattr(self.image, 'path') and 
        os.path.exists(self.image.path)):
            try:
                with Image.open(self.image.path) as img:
                    if img.height > 500 or img.width > 500:
                        output_size = (500, 500)
                        img.thumbnail(output_size)
                        img.save(self.image.path)
            except (IOError, OSError) as e:
                print(f"Could not process image: {e}")
    
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() # include an additional field for email
    
    class Meta:
        model = User # define model used for the form
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['image', 'desc']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desc'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tell us about your Pokemon journey...',
            'rows': 5
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control'
        })

