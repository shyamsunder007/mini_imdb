from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Languages)

admin.site.register(MovieLanguage)


admin.site.register(movie_role)


