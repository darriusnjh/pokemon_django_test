from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import Profile, UserUpdateForm, ProfileUpdateForm
from pokemaker.models import Pokemon

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account creared for {username}!')
            login(request, user)
            return redirect('poke_home')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def profile_view(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Get user's Pokemon count (adjust based on your Pokemon model)
    pokemon_count = Pokemon.objects.filter(owner=user).count() if hasattr(Pokemon, 'owner') else 0
    
    context = {
        'profile': profile,
        'pokemon_count': pokemon_count,
    }
    return render(request, 'users/profile.html', context)

@login_required
def my_profile_view(request):
    return profile_view(request, username=request.user.username)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('my_profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/edit_profile.html', context)
            