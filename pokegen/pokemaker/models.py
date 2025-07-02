from django import forms
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

POKEMON_TYPES = [
        ('normal', 'Normal'),
        ('fire', 'Fire'),
        ('water', 'Water'),
        ('electric', 'Electric'),
        ('grass', 'Grass'),
        ('ice', 'Ice'),
        ('fighting', 'Fighting'),
        ('poison', 'Poison'),
        ('ground', 'Ground'),
        ('flying', 'Flying'),
        ('psychic', 'Psychic'),
        ('bug', 'Bug'),
        ('rock', 'Rock'),
        ('ghost', 'Ghost'),
        ('dragon', 'Dragon'),
        ('dark', 'Dark'),
        ('steel', 'Steel'),
        ('fairy', 'Fairy'),
    ]


# Create your models here.
class Pokemon (models.Model):
    Name = models.CharField(max_length=20)
    desc = models.TextField()
    image = models.ImageField(default="bulbasaur.jpg", upload_to="poke pics")
    primary_type = models.CharField(max_length=20, choices=POKEMON_TYPES, default="normal")
    secondary_type = models.CharField(max_length=20, choices=POKEMON_TYPES, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    
    def get_absolute_url(self):
        return reverse('poke_detail', kwargs={'pk': self.pk})
    
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
    
class PokeUpdateForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['Name', 'desc']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['Name'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Enter Pokemon name'
            })
            self.fields['desc'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Describe your Pokemon...',
                'rows': 4
            })
            self.fields['image'].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['primary_type'].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['secondary_type'].widget.attrs.update({
                'class': 'form-control'
            })

class PokePromptForm(forms.Form):
    Name = forms.CharField(
        label="Name your Pokemon",
        widget=forms.Textarea({'rows':1}),
        max_length=30,
        required=True
    )
    look = forms.CharField(
        label="Describe your Pokemon color and look",
        widget=forms.Textarea(attrs={'placeholder': 'e.g. A green chimpanzee with leafy arms', 'rows': 3}),
        max_length=300,
        required=True
    )
    primary_type = forms.ChoiceField(
        label="Select Primary Type",
        choices=POKEMON_TYPES,
        widget=forms.Select,
        required=True
    )
    secondary_type = forms.ChoiceField( #this will return a list of strings
        label="Select Secondary Type",
        choices=[(None, 'No Secondary Type')] + POKEMON_TYPES,
        widget=forms.Select,
        required=False
    ) 
