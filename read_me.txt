mini_imdb:

Mini_imdb Django is a web app which serves as a Smaller version of Imdb with some addetion extra  filters.   
Database:-It scrape's data from IMDB website for only top 200 Indian Movie
It has the additoinal features such as:- 
	1)Top 20 Actors/Actresses appearing in these movies.
	2)Actors/Actresses appearing only once in any of these movies.
	3)Lead Actors/Actresses from any movie involved as crew of any other movie.
	4)Lead Actors/Actresses for a movie involved as crew of the same movie
	5)Above two tables for each language.
	6)Top 10 Actor-Director pair appearing in these movies.

For Setup Execute the following commands:-

git clone https://github.com/shyamsunder007/mini_imdb.git
cd mini_imdb
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Now check the localserver url('http://127.0.0.1:8000') in your web browser



Suggestion:-Please flush your data before updating the database:.
python manage.py flush
