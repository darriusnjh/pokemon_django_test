from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [ 
    path('', view=views.my_profile_view, name='my_profile'),
    path('<str:username>/', view=views.profile_view, name='profile'),
    path('edit', view=views.edit_profile, name='edit_profile')
]