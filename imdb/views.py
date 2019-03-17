from django.shortcuts import render
from .models import *
from bs4 import BeautifulSoup
import re
import requests
from django.db.models import Count
from django.db.models import F,Q
# Create your views here.
def get_role(x):
	if x==0:
		return "lead_actor"
	if x==1:
		return "director"
	if x==2:
		return "writer"
	return "crew"

def movie_list(request):
    complete_m=[]
    movie_objects=Movie.objects.all()
    
    for mov_object in movie_objects:
    	temp={}
    	temp["id"]=mov_object.id
    	temp["title"]=mov_object.title
    	temp["year"]=mov_object.year
    	temp["rating"]=mov_object.rating
    	temp["languages"]=[]
    	temp["lead_actors"]=[]
    	temp["crew"]=[]
    	temp["writers"]=[]
    	temp["directors"]=[]
    	get_language=MovieLanguage.objects.filter(movie=mov_object.id)
    	for lang in get_language:
    		obj=Languages.objects.filter(id=lang.lang_id)
    		temp["languages"].append(obj[0].language)
    	get_roles=movie_role.objects.filter(movie=mov_object.id)
    	for rol in get_roles:
    		per=Person.objects.filter(id=rol.person_id)[0].name
    		if rol.role==0:
    			temp["lead_actors"].append(per)
    		if rol.role==1:
    			temp["directors"].append(per)
    		if rol.role==2:
    			temp["writers"].append(per)
    		if rol.role==3:
    			temp["crew"].append(per)
    		#print (x.person,x.role)
    	temp["languages"]=",".join(temp["languages"])
    	temp["directors"]=",".join(temp["directors"])
    	temp["writers"]=",".join(temp["writers"])
    	temp["lead_actors"]=",".join(temp["lead_actors"])
    	temp["crew"]=",".join(temp["crew"])
    	
    	complete_m.append(temp)
    	#print (temp)
    return render(request, 'imdb/movie_list.html', {

        'movies': complete_m,
    })

    
def top20(request):
    actors=movie_role.objects.filter(role=0).values("person").annotate(the_count=Count("person")).order_by("-the_count")[:20]
    name_list=[]
    for actor in actors:
    	temp={}
    	#print (x['person'])
    	actor_name=Person.objects.filter(id=actor["person"])[0]
    	#print (actor_name.name,"name")
    	temp["name"]=actor_name.name
    	temp["the_count"]=actor["the_count"]
    	name_list.append(temp)
    return render(request, 'imdb/movie_top20.html', {

        'movies': name_list,
    })
def onlyonce(request):
    actors=movie_role.objects.filter(role=0).values("person").annotate(the_count=Count("person")).filter(the_count=1)
    name_list=[]
    for actor in actors:
    	temp={}
    	#print (x['person'])
    	actor_name=Person.objects.filter(id=actor["person"])[0]
    	#print (actor_name.name,"name")
    	temp["name"]=actor_name.name
    	temp["the_count"]=actor["the_count"]
    	name_list.append(temp)
    return render(request, 'imdb/movie_top20.html', {

        'movies': name_list,
    })
def involvedinother(request):
    complete=[]
    p_l=''
    if request.method == 'POST':
    	p_l=request.POST["lang"]
    	for p in movie_role.objects.raw('SELECT im1.person_id as id,im1.role as role1,im1.movie_id as movie1,im2.role as role2,im2.movie_id as movie2 FROM imdb_movie_role as im1  INNER join  imdb_movie_role as im2  on im1.person_id=im2.person_id where im1.role=0 and im2.role!=0 and im1.movie_id!=im2.movie_id'):
    		temp={}
    		actor_name=Person.objects.filter(id=p.id)[0]
    	#print (actor_name.name,"name")
    		temp["name"]=actor_name.name
    		movie_name=Movie.objects.filter(id=p.movie1)[0]
    	#print (actor_name.name,"name")
    		temp["movie_name1"]=movie_name.title
    		movie_name=Movie.objects.filter(id=p.movie2)[0]
    	#print (actor_name.name,"name")
    		temp["movie_name2"]=movie_name.title
    		temp["role1"]=get_role(p.role1)
    		temp["role2"]=get_role(p.role2)
    		lang3=Languages.objects.get(language=request.POST["lang"])
    		
    		lang1=MovieLanguage.objects.filter(movie=p.movie1,lang=lang3)
    		lang2=MovieLanguage.objects.filter(movie=p.movie2,lang=lang3)
    		if lang1 and lang2:
    			#print ("tre")
    			complete.append(temp)
    else:
    	for p in movie_role.objects.raw('SELECT im1.person_id as id,im1.role as role1,im1.movie_id as movie1,im2.role as role2,im2.movie_id as movie2 FROM imdb_movie_role as im1  INNER join  imdb_movie_role as im2  on im1.person_id=im2.person_id where im1.role=0 and im2.role!=0 and im1.movie_id!=im2.movie_id'):
    		temp={}
    		actor_name=Person.objects.filter(id=p.id)[0]
    	#print (actor_name.name,"name")
    		temp["name"]=actor_name.name
    		movie_name=Movie.objects.filter(id=p.movie1)[0]
    	#print (actor_name.name,"name")
    		temp["movie_name1"]=movie_name.title
    		movie_name=Movie.objects.filter(id=p.movie2)[0]
    	#print (actor_name.name,"name")
    		temp["movie_name2"]=movie_name.title
    		temp["role1"]=get_role(p.role1)
    		temp["role2"]=get_role(p.role2)
    		complete.append(temp)
    lang=[]
    for x in Languages.objects.all():
    	lang.append(x.language)
    return render(request, 'imdb/involvedinother.html', {

        'movies':complete ,'lang':lang,'pre_l':p_l
    })
def involvedinsame(request):
    complete=[]
    p_l=''
    if request.method == 'POST':
        p_l=request.POST["lang"]
        for p in movie_role.objects.raw('SELECT im1.person_id as id,im1.role as role1,im1.movie_id as movie1,im2.role as role2,im2.movie_id as movie2 FROM imdb_movie_role as im1  INNER join  imdb_movie_role as im2  on im1.person_id=im2.person_id where im1.role=0 and im2.role!=0 and im1.movie_id==im2.movie_id'):
        	temp={}
        	actor_name=Person.objects.filter(id=p.id)[0]
        	#print (actor_name.name,"name")
        	temp["name"]=actor_name.name
        	movie_name=Movie.objects.filter(id=p.movie1)[0]
	    	#print (actor_name.name,"name")
        	temp["movie_name1"]=movie_name.title
        	movie_name=Movie.objects.filter(id=p.movie2)[0]
        	#print (actor_name.name,"name")
        	temp["movie_name2"]=movie_name.title
        	temp["role1"]=get_role(p.role1)
        	temp["role2"]=get_role(p.role2)
        	lang3=Languages.objects.get(language=request.POST["lang"])
        	lang1=MovieLanguage.objects.filter(movie=p.movie1,lang=lang3)
        	lang2=MovieLanguage.objects.filter(movie=p.movie2,lang=lang3)
        	if lang1 and lang2:
        		#print ("tre")
        		complete.append(temp)
  
    else:
        for p in movie_role.objects.raw('SELECT im1.person_id as id,im1.role as role1,im1.movie_id as movie1,im2.role as role2,im2.movie_id as movie2 FROM imdb_movie_role as im1  INNER join  imdb_movie_role as im2  on im1.person_id=im2.person_id where im1.role=0 and im2.role!=0 and im1.movie_id==im2.movie_id'):
        	temp={}
        	actor_name=Person.objects.filter(id=p.id)[0]
        	#print (actor_name.name,"name")
        	temp["name"]=actor_name.name
        	movie_name=Movie.objects.filter(id=p.movie1)[0]
        	#print (actor_name.name,"name")
        	temp["movie_name1"]=movie_name.title
        	movie_name=Movie.objects.filter(id=p.movie2)[0]
	    	#print (actor_name.name,"name")
        	temp["movie_name2"]=movie_name.title
        	temp["role1"]=get_role(p.role1)
        	temp["role2"]=get_role(p.role2)
        	complete.append(temp)

    lang=[]
    for x in Languages.objects.all():
    	lang.append(x.language)
    return render(request, 'imdb/involvedinother.html', {

        'movies':complete ,'lang':lang,'pre_l':p_l
    })
def top10ad(request):
    complete=[]
    for p in movie_role.objects.raw('SELECT im1.id as id,im1.person_id as pid,im2.person_id as pid2,count(*) as c   FROM imdb_movie_role as im1  INNER join  imdb_movie_role as im2  on im1.movie_id=im2.movie_id where im1.role=0 and im2.role=1 and pid!=pid2 group by 2,3 order by c DESC Limit 10'):
    	temp={}
    	print (p.c)
    	actor_name=Person.objects.filter(id=p.pid)[0]
    	#print (actor_name.name,"name")
    	temp["name"]=actor_name.name

    	director_name=Person.objects.filter(id=p.pid2)[0]
    	#print (actor_name.name,"name")
    	temp["d_name"]=director_name.name
    
    	complete.append(temp)
    
    return render(request, 'imdb/top10ad.html', {

        'movies':complete ,
    })
def updatedb(request):
	# Download IMDB's Top 250 data
	url = 'https://www.imdb.com/india/top-rated-indian-movies/'
	#url='https://www.imdb.com/title/tt1734110/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=690bec67-3bd7-45a1-9ab4-4f274a72e602&pf_rd_r=MT42BCMRPTCZM7F89CC2&pf_rd_s=center-4&pf_rd_t=60601&pf_rd_i=india.top-rated-indian-movies&ref_=fea_india_ss_toprated_tt_250'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')

	movies = soup.select('td.titleColumn')
	links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
	crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
	ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
	votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

	imdb = []

	# Store each item into d5ictionary (data), then put those into a list (imdb)
	for index in range(0, 200):
	    # Seperate movie into: 'place', 'title', 'year'
	    #print (movies[index])
	    movie_string = movies[index].get_text()
	    movie = (' '.join(movie_string.split()).replace('.', ''))
	    movie_title = movie[len(str(index))+1:-7]
	    year = re.search('\((.*?)\)', movie_string).group(1)
	    links[index]='/'.join(links[index].split("/")[:3])
	    Language=[]
	    directors=[]
	    writers=[]
	    lead_star=crew[index].split(",")[1:]
	    print (lead_star)
	    place = movie[:len(str(index))-(len(movie))]
	    url="https://www.imdb.com"+links[index]
	    response = requests.get(url)
	    soup = BeautifulSoup(response.text, 'lxml')
	    header = soup.find("h4", text="Language:")
	    for item in header.next_siblings:
	        temp=str(item).split(">")
	        if len(temp)>1:
	            if len(temp[1].split("<")[0])>1:
	                Language.append(temp[1].split("<")[0])
	        if getattr(item, 'name') == 'h4' and item.text == 'Release Date:':
	            break
	    url="https://www.imdb.com"+links[index]+'/fullcredits/?ref_=tt_ov_st_sm'
	    response = requests.get(url)
	    soup = BeautifulSoup(response.text, 'lxml')
	    asd=soup.findAll('table', attrs={'class':'simpleTable simpleCreditsTable'})
	#    print div.a['href']
	    for x in asd[0].findAll('a'):
	        directors.append(x.text[:-1])

	    for x in asd[1].findAll('a'):
	        writers.append(x.text[:-1])
	    asd=soup.findAll('table', attrs={'class':'cast_list'})
	#    print div.a['href']
	#print (asd[0].findAll('a'))
	    other_crew=[]
	    for x in asd[0].findAll('a'):
	        temp=x.text
	        if "\n" in x.text:
	            temp=x.text[:-1]
	        if temp not in lead_star and len(x.text)>1:
	            other_crew.append(temp)
	    
	    data = {"movie_title": movie_title,
	            "year": year,
	            "place": place,
	            "star_cast": lead_star,
	            "rating": ratings[index],
	            "vote": votes[index],
	            "link": links[index],
	            "Languages":Language,
	            "Writer":writers,
	            "Directors":directors,
	            "crew":other_crew[:10]}
	    #print (data)  
	    imdb.append(data)

	for item in imdb:
		if not (Movie.objects.get(title=item['movie_title'])):
		    movie_id=Movie.objects.create(title=item['movie_title'],year=int(item['year']),rating=round(float(item["rating"]),2))
		    for x in item['Languages']:
		    	lid=Languages.objects.filter(language=x)
		    	if lid:
		    		lid=Languages.objects.get(language=x)
		    		MovieLanguage.objects.create(movie=movie_id,lang=lid)
		    	else:
		    		lid=Languages.objects.create(language=x)
		    		MovieLanguage.objects.create(movie=movie_id,lang=lid)
		    for x in item["star_cast"]:
		    	pid=Person.objects.filter(name=x)
		    	if pid:
		    		pid=Person.objects.get(name=x)
		    		movie_role.objects.create(person=pid,movie=movie_id,role=0)
		    	else:
		    		pid=Person.objects.create(name=x)
		    		movie_role.objects.create(person=pid,movie=movie_id,role=0)

		    for x in item["Directors"]:
		    	pid=Person.objects.filter(name=x)
		    	if pid:
		    		pid=Person.objects.get(name=x)
		    		movie_role.objects.create(person=pid,movie=movie_id,role=1)
		    	else:
		    		pid=Person.objects.create(name=x)
		    		movie_role.objects.create(person=pid,movie=movie_id,role=1)
		    for x in item["Writer"]:
		    	pid=Person.objects.filter(name=x)
		    	if pid:
		    		pid=Person.objects.get(name=x)
		    		movie_role.objects.create(person=pid,movie=movie_id,role=2)
		    	else:
		    		pid=Person.objects.create(name=x)
		    		movie_role.objects.create(person=pid,movie=movie_id,role=2)
		    for x in item["crew"]:
		    	pid=Person.objects.filter(name=x)
		    	if pid:
		    		pid=Person.objects.get(name=x)
		    		movie_role.objects.create(person=pid,movie=movie_id,role=3)
		    	else:
		    		pid=Person.objects.create(name=x)
		    		movie_role.objects.create(person=pid,movie=movie_id,role=3)
		print ("Progresing:---")    
		#print(item['place'] ,'-',item['movie_title'], '('+item['year']+') -', 'Starring:', item['Languages'],"-",round(float(item["rating"]),2))
	return render(request, 'imdb/involvedinother.html', {

        
    })