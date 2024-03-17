from pymongo import GEOSPHERE

class TheaterCollection:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection = self.db['theaters']
    
    def top_10_cities_with_max_theaters(self):
        pipeline = [
            {"$match": {"location.address.city": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": "$location.address.city", "theater_count": {"$sum": 1}}},
            {"$sort": {"theater_count": -1}},
            {"$limit": 10}
        ]
        top_cities = list(self.collection.aggregate(pipeline))
        return top_cities

    def top_10_theatres_nearby(self, coordinates):
        self.collection.create_index([("location.geo", GEOSPHERE)])
        pipeline = [
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": coordinates
                    },
                    "distanceField": "distance",
                    "spherical": True,
                    "maxDistance": 10000  # Maximum distance in meters
                }
            },
            {"$limit": 10},  # Limit the results to 10 nearest theaters
            {
                "$project": {
                    "_id": 0,
                    "theaterId": 1,
                    "location": 1
                }
            }
        ]
        nearest_theatres = list(self.collection.aggregate(pipeline))
        return nearest_theatres
    
    def add_theater(self):
        # Prompt user for input
        theater_id = int(input("Enter the theater ID: "))
        street1 = input("Enter street address: ")
        city = input("Enter city: ")
        state = input("Enter state: ")
        zipcode = input("Enter zipcode: ")
        longitude = float(input("Enter longitude: "))
        latitude = float(input("Enter latitude: "))

        # Create the location document
        location = {
            "address": {
                "street1": street1,
                "city": city,
                "state": state,
                "zipcode": zipcode
            },
            "geo": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            }
        }

        # Create the theater document
        theater = {
            "theaterId": theater_id,
            "location": location
        }

        # Insert the theater into the collection
        self.collection.insert_one(theater)

        # Print success message
        print("Theater added successfully!")




