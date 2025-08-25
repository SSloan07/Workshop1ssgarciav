from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt 
import matplotlib
import io
import urllib, base64 

from .models import Movie
# Create your views here.
def home(request): 
    # return render(request,'home.html', {'name':'Simón Sloan García Villa :)'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm: 
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})

def about(request): 
    return render(request,'about.html')
def statistics_view (request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') 
    movie_counts_by_year = {}
    for year in years: 
        if year: 
            movies_in_year = Movie.objects.filter(year=year)
        else: 
            movies_in_year =Movie.objects.filter(year_isnull=True) 
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count
    
    bar_width = 0.5 
    bar_spacing = 0.5 
    bar_positions = range (len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align = "center")

    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(),rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue() 
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    genres_raw = Movie.objects.values_list('genre', flat=True).exclude(genre__isnull=True).exclude(genre='')

    movie_counts_by_genre = {}

    for genre_value in genres_raw:
        first_genre = genre_value.split(',')[0].strip()  # Tomar solo el primer género

        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    
    bar_width = 0.5 
    bar_spacing = 0.5 
    bar_positions = range (len(movie_counts_by_genre))
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align = "center")

    plt.title('Movies per genre(first only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(),rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    plt.close()

    imageGenre_png = buffer.getvalue() 
    buffer.close()
    graphicGenre = base64.b64encode(imageGenre_png)
    graphicGenre= graphicGenre.decode('utf-8')
    return render(request, 'statistics.html', {
    'graphic': graphic,
    'graphicGenre': graphicGenre
    })

