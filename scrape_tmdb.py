import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYWE2NDI3M2M3ODFlMzc3YmE4YTAwMzEwMWQwZmE0YSIsInN1YiI6IjY2NTJiNzc2MmQwZDA2YmMwZTcxYTRiNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.aIRuRs7JKJkANnWq9di2M2PL-a9Fbb3pkPGbYt6U0UE"
}

def get_toprated_movies():    
    movie_ids = []
    for i in range(1, 472):
        url = f"https://api.themoviedb.org/3/movie/top_rated?language=english&page={i}"
        response = requests.get(url, headers=headers)
        data = response.json()
        for movie in data['results']:
            movie_ids.append(movie['id'])
    print(len(movie_ids))
    return movie_ids

def fetch_movie_detail(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=credits&language=en-US"    
    response = requests.get(url, headers=headers)
    movie = response.json()
    credits = movie['credits']
    title = movie['title']
    budget = '$' + f"{movie['budget']:,}"
    cast = credits['cast'][0:20]
    actors = [i['name'] for i in cast]
    production_companies = [i['name'] for i in movie['production_companies']]
    genres = [genre['name'] for genre in movie['genres']]
    rating = movie['vote_average']
    revenue = '$' + f"{movie['revenue']:,}"
    # if movie belongs to collection, set to true, else false
    series = movie['belongs_to_collection'] is not None
    
    return {
        'title': title,
        'budget': budget,
        'genres': genres,
        'actors': actors,
        'production_companies': production_companies,
        'rating': rating,
        'revenue': revenue,
        'series': series
    }

def get_movie_details(movie_ids):
    #To speed up the process, we can use multithreading to fetch movie details concurrently
    movie_details = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_movie_detail, movie_id) for movie_id in movie_ids]
        for future in as_completed(futures):
            try:
                movie_details.append(future.result())
            except Exception as e:
                print(f"An error occurred: {e}")
    return movie_details

def scrape_tmdb():
    movie_ids = get_toprated_movies()
    print(len(movie_ids))
    movie_details = get_movie_details(movie_ids)

    with open('top_rated_movies.csv', 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Budget", "Genres", "Actors","Production Companies", "Rating", "Revenue", "Series"])
        for movie in movie_details:
            writer.writerow([movie['title'], movie['budget'], movie['genres'], movie['actors'], movie['production_companies'], movie['rating'], movie['revenue'], movie['series']])
scrape_tmdb()
