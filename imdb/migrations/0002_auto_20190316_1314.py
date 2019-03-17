# Generated by Django 2.1 on 2019-03-16 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imdb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='director',
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ManyToManyField(blank=True, related_name='director', to='imdb.Person'),
        ),
    ]
