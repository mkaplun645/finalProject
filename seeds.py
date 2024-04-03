from flask_seeder import Seeder, generator
from faker import Faker
from app import create_app, db
from models import User, Listing, Contact

fake=Faker()
app = create_app()

# User Seeder
class UserSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)

    def generate_username(self):
        return fake.user_name()

    def generate_first_name(self):
        return fake.first_name()

    def generate_last_name(self):
        return fake.last_name()

    def generate_user_type(self):
        return fake.random_element(elements=('Buyer', 'Seller'))

    def generate_email(self):
        return fake.email()

    def run(self):
        users_data = []

        for _ in range(10):
            user_data = {
                'username': self.generate_username(),
                'first_name': self.generate_first_name(),
                'last_name': self.generate_last_name(),
                'user_type': self.generate_user_type(),
                'email': self.generate_email(),
            }
            users_data.append(user_data)

        self.add_entity(User, users_data)

seeder = UserSeeder(db=db)

seeder.run()

# Listing Seeder
# class ListingSeeder(Seeder):
#     def run(self):
#         faker = Faker(
#             cls=Listing,
#             init={
#                 "title": generator.String("title", length=5),
#                 "description": generator.String("description", length=20),

#             }
#         )