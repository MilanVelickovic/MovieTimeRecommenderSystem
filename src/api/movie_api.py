import requests

class MovieAPI:
    def __init__(self):
        self.base_url = "https://api.themoviedb.org/3/"
        self.api_key = "508a1d40f3911f5d61fa8f25fe4def49"

    def getMovieGenres(self):
        # Example: https://api.themoviedb.org/3/genre/movie/list?api_key=<<API_KEY>>
        return requests.get(self.base_url + "genre/movie/list?api_key=" + self.api_key).json()
    
    def getMoviesByGenre(self, genreId):
        # Example: https://api.themoviedb.org/3/discover/movie?api_key=<<API_KEY>>&with_genres=28
        return requests.get(self.base_url + "discover/movie?api_key=" + self.api_key + "&with_genres=" + str(genreId)).json()

