from django.db import models

# Create your models here.
class Movie(models.Model):
   
    title = models.CharField(max_length=200,unique=True)
    year = models.PositiveIntegerField()
    rating = models.FloatField()
    def __str__(self):
        return self.title
    
class Languages(models.Model):
    language=models.CharField(max_length=200,unique=True)
    def __str__(self):
        return ('{0},{1}'.format(self.language,self.id))
class MovieLanguage(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    lang=models.ForeignKey(Languages,on_delete=models.CASCADE)
    def __str__(self):
        return ('{}'.format(self.id))


class Person(models.Model):
    name=models.CharField(max_length=200,unique=True)
    def __str__(self):
        return ('{0}'.format(self.id))
class movie_role(models.Model):
    lead_actors = 0
    directors = 1
    writers = 2
    crew = 3
    ROLES = (
        (lead_actors, 'Lead_actor'),
        (directors, 'Director'),
        (writers, 'Writer'),
        (crew, 'CREW'),
    )
    person=models.ForeignKey(Person,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    role=models.IntegerField(choices=ROLES, default=crew)
    def __str__(self):
        return ('{0}'.format(self.id))
