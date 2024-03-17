class UserCollection:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection = self.db['users']

    def add_user(self):
        # Prompt user for input
        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        # Create the user document
        user = {
            "name": name,
            "email": email,
            "password": password
        }

        # Insert the user into the collection
        self.collection.insert_one(user)

        # Print success message
        print("User added successfully!")