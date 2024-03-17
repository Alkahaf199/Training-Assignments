from queries.theatre_queries import TheaterCollection
from queries.movies_queries import MovieCollection
from queries.comments_queries import CommentCollection
from queries.users_queries import UserCollection
from loadFiles import load_json_files
from databaseConnect import Database

def main():

    db_connection = Database()

    # Load JSON files into the database
    json_dir = './jsonData/sample_mflix'
    load_json_files(json_dir, db_connection)

    theater_manager = TheaterCollection(db_connection)
    comment_manager = CommentCollection(db_connection)
    movie_manager = MovieCollection(db_connection)
    user_manager = UserCollection(db_connection)

    while True:
        print("Select a category:")
        print("1. Theater Management")
        print("2. Movie Database")
        print("3. Comments")
        print("4. Users")
        print("5. Exit")

        category_choice = input("Enter your choice: ")

        if category_choice == '1':
            while True:
                print("\nSelect an option for Theater Management:")
                print("1. Top 10 cities with the maximum number of theaters")
                print("2. Top 10 theatres nearby given coordinates")
                print("3. Add Theatre")
                print("4. Back")

                theater_choice = input("Enter your choice: ")

                if theater_choice == '1':
                    top_cities = theater_manager.top_10_cities_with_max_theaters()
                    print("Top 10 cities with the maximum number of theaters:")
                    for city in top_cities:
                        print(city)

                elif theater_choice == '2':
                    use_default = input("Do you want to use default coordinates? (yes/no): ").lower()
                    if use_default == 'yes':
                        # Default coordinates (e.g., latitude and longitude)
                        default_coordinates = [-93.24565, 44.85466] # Example coordinates (New York City)
                        nearby_theatres = theater_manager.top_10_theatres_nearby(default_coordinates)
                    else:
                        # User inputs custom coordinates
                        latitude = float(input("Enter latitude: "))
                        longitude = float(input("Enter longitude: "))
                        user_coordinates = [latitude, longitude]
                        nearby_theatres = theater_manager.top_10_theatres_nearby(user_coordinates)

                    # Display top 10 theaters nearby
                    print("Top 10 Theaters Nearby:")
                    print(nearby_theatres)

                elif theater_choice == '3':
                    theater_manager.add_theater()

                elif theater_choice == '4':
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

        elif category_choice == '2':
            while True:
                print("\nSelect a category:")
                print("1. Movies")
                print("2. Directors")
                print("3. Actors")
                print("4. Find top `N` movies for each genre with the highest IMDB rating")
                print("5. Add Movie")
                print("6. Back")

                category = input("Enter your choice: ")

                if category == '1':
                    while True:
                        print("\nSelect an option for Movie Database:")
                        print("1. Top N movies by IMDb rating")
                        print("2. Top N movies by IMDb rating in a specific year")
                        print("3. Top N movies by IMDb rating with number of votes > 1000")
                        print("4. Top N movies with title matching a given pattern sorted by highest tomatoes ratings")
                        print("5. Back")

                        movie_choice = input("Enter your choice: ")



                        if movie_choice == '1':
                            N = int(input("Enter the number of top movies you want to see: "))
                            top_movies = movie_manager.top_n_movies_by_imdb(N)
                            print(f"Top {N} movies by IMDb rating:")
                            print(top_movies)

                        elif movie_choice == '2':
                            year = int(input("Enter the year: "))
                            N = int(input("Enter the number of top movies you want to see: "))
                            top_movies = movie_manager.top_n_movies_by_imdb_year(year, N)
                            print(f"Top {N} movies by IMDb rating in {year}:")
                            print(top_movies)

                        elif movie_choice == '3':
                            N = int(input("Enter the number of top movies you want to see: "))
                            top_movies = movie_manager.top_n_movies_by_imdb_vote(N)
                            print(f"Top {N} movies by IMDb rating with number of votes > 1000:")
                            print(top_movies)
                            
                        elif movie_choice == '4':
                            title = input("Enter a title: ")
                            N = int(input("Enter the number of top movies you want to see: "))
                            top_movies = movie_manager.top_n_movies_by_title_tomatoes(title, N)
                            print(f"Top {N} movies with title matching a given pattern sorted by highest tomatoes ratings: ")
                            print(top_movies)
                            
                        elif movie_choice == '5':    
                            movie_manager.add_movie()

                        elif movie_choice == '6':    
                            break
                        else:
                            print("Invalid choice. Please enter a valid option.")

                elif category == '2':
                    while True:
                        print("1. Find top `N` directors who created the maximum number of movies.")
                        print("2. Find top `N` directors who created the maximum number of movies in a given year.")
                        print("3. Find top `N` directors who created the maximum number of movies for a given genre.")
                        print("4. Back")

                        director_choice = input("Enter your choice: ")

                        if director_choice == '1':
                            N = int(input("Enter the number of top directors who created the maximum number of movies: "))
                            top_directors = movie_manager.top_n_directors_by_movies(N)
                            print(f"Top {N} directors who created the maximum number of movies.")
                            print(top_directors)

                        elif director_choice == '2':
                            N = int(input("Enter the number of top directors who created the maximum number of movies in a given year: "))
                            year = int(input("Enter the year: "))
                            top_directors = movie_manager.top_n_directors_by_movies_in_year(year, N)
                            print(f"Top {N} directors who created the maximum number of movies in a given year.")
                            print(top_directors)

                        elif director_choice == '3':
                            N = int(input("Enter the number of top directors who created the maximum number of movies for a given genre: "))
                            genre = input("Enter the genre: ")
                            top_directors = movie_manager.top_n_directors_by_movies_for_genre(genre, N)
                            print(f"Top {N} directors who created the maximum number of movies for a given genre.")
                            print(top_directors)


                        elif director_choice == '4':
                            break
                        
                        else:
                            print("Invalid choice. Please enter a valid option.")

                elif category == '3':
                    while True:
                        print("1. Find top `N` actors who created the maximum number of movies.")
                        print("2. Find top `N` actors who created the maximum number of movies in a given year.")
                        print("3. Find top `N` actors who created the maximum number of movies for a given genre.")
                        print("4. Back")

                        actor_choice = input("Enter your choice: ")

                        if actor_choice == '1':
                            N = int(input("Enter the number of top actors who created the maximum number of movies: "))
                            top_actors = movie_manager.top_n_actors_by_movies(N)
                            print(f"Top {N} actors who created the maximum number of movies.")
                            print(top_actors)

                        elif actor_choice == '2':
                            N = int(input("Enter the number of top actors who created the maximum number of movies in a given year: "))
                            year = int(input("Enter the year: "))
                            top_actors = movie_manager.top_n_actors_by_movies_in_year(year, N)
                            print(f"Top {N} actors who created the maximum number of movies in a given year.")
                            print(top_actors)

                        elif actor_choice == '3':
                            N = int(input("Enter the number of top actors who created the maximum number of movies for a given genre: "))
                            genre = input("Enter the genre: ")
                            top_actors = movie_manager.top_n_actors_by_movies_for_genre(genre, N)
                            print(f"Top {N} actors who created the maximum number of movies for a given genre.")
                            print(top_actors)


                        elif director_choice == '4':
                            break
                        
                        else:
                            print("Invalid choice. Please enter a valid option.")

                        

                elif category == '4':
                    N = int(input("Enter the number of top movies you want to see: "))
                    top_movies = movie_manager.top_n_movies_by_genre_and_imdb_rating(N)
                    print(f"Top {N} movies for each genre with the highest IMDB rating")
                    print(top_movies)

                    
                elif category == '5':
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

        elif category_choice == '3':
            while True:
                print("\nSelect an option for Comments:")
                print("1. Find top ten commentors")
                print("2. Find top ten commented movies")
                print("3. Find total comments for a specific year")
                print("4. Add Comments")
                print("5. Back")

                comment_choice = input("Enter your choice: ")

                if comment_choice == '1':
                    top_commenters = comment_manager.find_top_ten_commentors()
                    print("Top ten commenters:")
                    print(top_commenters)

                elif comment_choice == '2':
                    top_commented_movies = comment_manager.find_top_ten_commented_movies()
                    print("Top ten commented movies:")
                    top_commented_movies = movie_manager.get_movie_names_by_ids(top_commented_movies)
                    print(top_commented_movies)

                elif comment_choice == '3':
                    year = int(input("Enter the year: "))
                    total_comments = comment_manager.find_total_comments_year(year)
                    print(f"Total comments for year {year}:")
                    print(total_comments)

                elif comment_choice == '4':
                    comment_manager.add_comment()

                elif comment_choice == '5':
                    break

                else:
                    print("Invalid choice. Please enter a valid option.")

        elif category_choice == '4':
            user_manager.add_user()

        elif category_choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()


