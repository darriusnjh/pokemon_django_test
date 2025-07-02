from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from .models import Pokemon, PokeUpdateForm, PokePromptForm
from django.core.paginator import Paginator
from .service.diffusion_service import DiffusionService
import os

# Create your views here.
def user_pokemons(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    paginator = Paginator(Pokemon.objects.filter(owner=user), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'profile': user.profile,
    }

    return render(request, 'pokemaker/user_pokemon.html', context)

@login_required
def poke_prompt(request):
    if request.method == 'POST':
        user = request.user
        form = PokePromptForm(request.POST)
        if form.is_valid():
            Name = form.cleaned_data['Name']
            look = form.cleaned_data['look']
            types = []
            types.append(form.cleaned_data['primary_type'])
            if form.cleaned_data['secondary_type']:
                types.append(form.cleaned_data['secondary_type'])
            types_str = " and ".join(types)
            prompt = f"{look} of type {types_str}"
            diffusion = DiffusionService()
            image_path = "generated_poke/Catopus.png"  # diffusion.generate_image(prompt, Name)

            pokemon = Pokemon.objects.create(Name=Name,
                                             desc="",
                                             image=image_path,
                                             primary_type=types[0],
                                             secondary_type=types[1] if len(types)>1 else None,
                                             owner=user
                                             )
            try:
                os.remove("media/"+image_path)
            except Exception as e:
                print(e)

            return redirect('poke_detail', pk=pokemon.pk) # this will define where the submit button takes the user
    else:
        form = PokePromptForm()
    
    return render(request, 'pokemaker/poke_prompter.html', {'form':form})   



class PokeListView(ListView):
    model = Pokemon
    template_name = 'pokemaker/home.html'
    context_object_name = 'pokemons'
    ordering = ['Name']
    paginate_by = 10

class PokeDetailView(DetailView):
    model = Pokemon

class PokeCreateView(LoginRequiredMixin, CreateView):
    model = Pokemon
    template_name = 'pokemaker/poke_create.html'
    fields = ['Name', 'desc', 'image', 'primary_type', 'secondary_type']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PokeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pokemon
    form_class = PokeUpdateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        pokemon = self.get_object()
        return self.request.user == pokemon.owner
    
class PokeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pokemon
    success_url = '/'

    def test_func(self):
        pokemon = self.get_object()
        return self.request.user == pokemon.owner

    