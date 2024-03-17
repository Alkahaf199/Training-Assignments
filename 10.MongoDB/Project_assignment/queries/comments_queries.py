
import datetime


class CommentCollection:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection = self.db['comments']

    def find_top_ten_commentors(self):
        top_commenters = self.collection.aggregate([
            {"$group": {"_id": "$name", "total_comments": {"$sum": 1}}},
            {"$sort": {"total_comments": -1}},
            {"$limit": 10}
        ])
        return list(top_commenters)

    def find_top_ten_commented_movies(self):
        top_commented_movies = self.collection.aggregate([
            {"$group": {"_id": "$movie_id", "total_comments": {"$sum": 1}}},
            {"$sort": {"total_comments": -1}},
            {"$limit": 10}
        ])
        return list(top_commented_movies)

    def find_total_comments_year(self, year):
        pipeline = [
            {"$match": {"$expr": {"$eq": [{"$year": "$date"}, year]}}},
            {"$group": {
                "_id": {"month": {"$month" : "$date"}},
                "total_comments": {"$sum": 1}
            }},
            {"$sort": {"_id.month": 1}}
        ]
        total_comments = self.collection.aggregate(pipeline)
        return list(total_comments)
    
    def add_comment(self):
        # Prompt user for input
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        movie_id = input("Enter the movie ID: ")  # Assuming movie_id is a string
        text = input("Enter your comment: ")
        date = datetime.utcnow()

        # Create the comment document
        comment = {
            "name": name,
            "email": email,
            "movie_id": movie_id,
            "text": text,
            "date": date
        }

        # Insert the comment into the collection
        self.collection.insert_one(comment)

        # Print success message
        print("Comment added successfully!")