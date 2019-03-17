from django.urls import path
from . import views

app_name = 'imdb'

urlpatterns = [
    path('',  views.movie_list, name='movie_list'),

    path('home/',  views.updatedb, name='update_db'),
    path('top20/',  views.top20, name='top20'),
    path('onlyonce/',  views.onlyonce, name='onlyonce'),
	path('involvedinother/',  views.involvedinother, name='involvedinother'),
	path('involvedinsame/',  views.involvedinsame, name='involvedinsame'),
    path('top10ad/',  views.top10ad, name='top10ad'),
   
  ]

