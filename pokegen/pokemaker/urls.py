from django.contrib import admin
from django.urls import path
from . import views
from .views import PokeDetailView, PokeUpdateView, PokeCreateView, PokeDeleteView, PokeListView

urlpatterns = [
    path('', view=PokeListView.as_view(), name='poke_home'),
    path('poke/create', view = PokeCreateView.as_view(), name='poke_create'),
    path('poke/<int:pk>/', view = PokeDetailView.as_view(), name='poke_detail'),
    path('poke/<int:pk>/update/', view = PokeUpdateView.as_view(), name='poke_update'),
    path('poke/<int:pk>/delete/', view = PokeDeleteView.as_view(), name='poke_delete'),
    path('poke/<str:username>/', view = views.user_pokemons, name='poke_user'),
    path('poke/prompt', view=views.poke_prompt, name='poke_prompt')
]