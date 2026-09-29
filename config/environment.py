import os

DATABASE_URL = os.getenv('DATABASE_URL')
JWT_SECRET = os.getenv('JWT_SECRET')


db_URI = "postgresql+psycopg2://hasan:Hasan.2003@localhost:5432/movies_db"