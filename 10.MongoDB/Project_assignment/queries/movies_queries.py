import datetime

from bson import ObjectId


class MovieCollection:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection = self.db['movies']

    def top_n_movies_by_imdb(self, N):
        pipeline = [
            {"$match": {"imdb.rating": {"$exists": True, "$ne": ""}}},
            {"$group": {"_id": "$title", "imdb_rating": {"$max": "$imdb.rating"}}},  
            {"$sort": {"imdb_rating": -1}},
            {"$limit": N},
            {"$project": {"_id": 0, "movie_name": "$_id", "imdb_rating": 1}}
        ]
        top_movies = self.collection.aggregate(pipeline)
        return list(top_movies)

    def top_n_movies_by_imdb_year(self, year, N):
        pipeline = [
            {"$match": {"year": year, "imdb.rating": {"$exists": True}}},
            {"$sort": {"imdb.rating": -1}},
            {"$limit": N},
            {"$project": {"_id": 0, "movie_name": "$title", "imdb_rating": "$imdb.rating"}}
        ]
        top_movies = self.collection.aggregate(pipeline)
        return list(top_movies)

    def top_n_movies_by_imdb_vote(self, N):
        pipeline = [
            {"$match": {"imdb.rating": {"$exists": True}, "imdb.votes": {"$exists": True, "$gt": 1000}}},
            {"$group": {"_id": "$title", "imdb_rating": {"$first": "$imdb.rating"}, "votes": {"$first": "$imdb.votes"}}},
            {"$sort": {"imdb_rating": -1}},
            {"$limit": N},
            {"$project": {"_id": 0, "movie_name": "$_id", "imdb_rating": 1, "votes": 1}}
        ]
        top_movies = self.collection.aggregate(pipeline)
        return list(top_movies)

    def top_n_movies_by_title_tomatoes(self, title, N):
        pipeline = [
            {"$match": {"title": {"$regex": r'\b' + title + r'\b', "$options": "i"}, "tomatoes.viewer.rating": {"$exists": True}}},
            {"$sort": {"tomatoes.viewer.rating": -1}},
            {"$limit": N},
            {"$project": {"_id": 0, "movie_name": "$title", "tomatoes_rating": "$tomatoes.viewer.rating"}}
        ]
        top_movies = self.collection.aggregate(pipeline)
        return list(top_movies)

    def top_n_directors_by_movies(self, N):
        pipeline = [
            {"$match": {"directors": {"$exists": True, "$ne": None}}},  
            {"$unwind": "$directors"},  
            {"$group": {"_id": "$directors", "movie_count": {"$sum": 1}}},  
            {"$project": {"_id": 0, "director": "$_id", "movie_count": 1}}, 
            {"$sort": {"movie_count": -1}},  
            {"$limit": N}
        ]
        top_directors = list(self.collection.aggregate(pipeline))
        return top_directors

    def top_n_directors_by_movies_in_year(self, year, N):
        pipeline = [
            {"$match": {"year": year, "directors": {"$exists": True, "$ne": None}}},  
            {"$unwind": "$directors"},  
            {"$group": {"_id": "$directors", "movie_count": {"$sum": 1}}},  
            {"$project": {"_id": 0, "director": "$_id", "movie_count": 1}},  
            {"$sort": {"movie_count": -1}},  
            {"$limit": N}
        ]
        top_directors = list(self.collection.aggregate(pipeline))
        return top_directors

    def top_n_directors_by_movies_for_genre(self, genre, N):
        pipeline = [
            {"$match": {
                "genres": {"$exists": True, "$ne": None},
                "genres": {"$regex": genre, "$options": "i"}
            }},
            {"$unwind": "$directors"},  
            {"$group": {"_id": "$directors", "movie_count": {"$sum": 1}}},  
            {"$project": {"_id": 0, "director": "$_id", "movie_count": 1}},  
            {"$sort": {"movie_count": -1, "_id": 1}},  
            {"$limit": N}
        ]
        top_directors = self.collection.aggregate(pipeline)
        return list(top_directors)


    def top_n_actors_by_movies(self, N):
        pipeline = [
            {"$match": {"cast": {"$exists": True, "$ne": None}}},  
            {"$unwind": "$cast"},
            {"$group": {"_id": "$cast", "movie_count": {"$sum": 1}}},
            {"$project": {"_id": 0, "cast": "$_id", "movie_count": 1}},
            {"$sort": {"movie_count": -1}},
            {"$limit": N}
        ]
        return list(self.collection.aggregate(pipeline))

    def top_n_actors_by_movies_in_year(self, year, N):
        pipeline = [
            {"$match": {"year": year, "cast": {"$exists": True, "$ne": None}}},
            {"$unwind": "$cast"},
            {"$group": {"_id": "$cast", "movie_count": {"$sum": 1}}},
            {"$project": {"_id": 0, "actor": "$_id", "movie_count": 1}},
            {"$sort": {"movie_count": -1}},
            {"$limit": N}
        ]
        return list(self.collection.aggregate(pipeline))

    def top_n_actors_by_movies_for_genre(self, genre, N):
        pipeline = [
            {"$match": {"genres": {"$exists": True, "$ne": None}, "genres": {"$regex": genre, "$options": "i"}}},
            {"$unwind": "$cast"},
            {"$group": {"_id": "$cast", "movie_count": {"$sum": 1}}},
            {"$project": {"_id": 0, "actor": "$_id", "movie_count": 1}},
            {"$sort": {"movie_count": -1, "_id": 1}},
            {"$limit": N}
        ]
        return list(self.collection.aggregate(pipeline))

    def top_n_movies_by_genre_and_imdb_rating(self, N):
        pipeline = [
            {"$match": {"imdb.rating": {"$exists": True}, "genres": {"$exists": True}}},
            {"$unwind": "$genres"},
            {"$sort": {"genres": 1, "imdb.rating": -1}},
            {"$group": {"_id": "$genres", "movies": {"$push": {"title": "$title", "imdb_rating": "$imdb.rating"}}}},
            {"$project": {"_id": 0, "genre": "$_id", "top_movies": {"$slice": ["$movies", N]}}}
        ]
        return list(self.collection.aggregate(pipeline))
    
    def add_movie(self):
        # Prompt user for input
        title = input("Enter the movie title: ")
        plot = input("Enter the plot summary: ")
        genres = input("Enter genres (comma-separated): ").split(',')
        runtime = int(input("Enter the runtime (in minutes): "))
        cast = input("Enter cast members (comma-separated): ").split(',')
        num_mflix_comments = int(input("Enter the number of comments: "))
        countries = input("Enter countries (comma-separated): ").split(',')
        director = input("Enter director's name: ")
        rated = input("Enter the rating: ")
        wins = int(input("Enter the number of awards won: "))
        nominations = int(input("Enter the number of award nominations: "))
        imdb_rating = float(input("Enter the IMDb rating: "))
        imdb_votes = int(input("Enter the IMDb votes: "))
        tomatoes_viewer_rating = float(input("Enter the viewer rating on Rotten Tomatoes: "))
        tomatoes_num_reviews = int(input("Enter the number of reviews on Rotten Tomatoes: "))
        tomatoes_meter = int(input("Enter the meter score on Rotten Tomatoes: "))
        last_updated = datetime.utcnow()

        # Create the movie document
        movie = {
            "title": title,
            "plot": plot,
            "genres": genres,
            "runtime": runtime,
            "cast": cast,
            "num_mflix_comments": num_mflix_comments,
            "countries": countries,
            "directors": [director],
            "rated": rated,
            "awards": {
                "wins": wins,
                "nominations": nominations,
                "text": f"{wins} win(s), {nominations} nomination(s)"
            },
            "year": last_updated.year,
            "imdb": {
                "rating": imdb_rating,
                "votes": imdb_votes,
                "id": None  # Add IMDb ID if available
            },
            "type": "movie",
            "tomatoes": {
                "viewer": {
                    "rating": tomatoes_viewer_rating,
                    "numReviews": tomatoes_num_reviews,
                    "meter": tomatoes_meter
                },
                "lastUpdated": last_updated
            }
        }

        # Insert the movie into the collection
        self.collection.insert_one(movie)

        # Print success message
        print("Movie added successfully!")

    def get_movie_names_by_ids(self, movie_ids):
        movie_names = []
        for movie_id_dict in movie_ids:
            movie_id = movie_id_dict['_id']
            movie_id = ObjectId(movie_id)  # Convert the string ID to ObjectId
            movie = self.collection.find_one({"_id": movie_id}, {"title": 1})
            if movie:
                movie_names.append(movie['title'])
            else:
                movie_names.append("Unknown")
        return movie_names