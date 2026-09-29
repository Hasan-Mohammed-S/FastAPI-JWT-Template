from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from controllers.movies import router as MoviesRouter
from controllers.reviews import router as ReviewsRouter
from controllers.users import router as UsersRouter

app = FastAPI()

app.include_router(MoviesRouter, prefix='/api')
app.include_router(ReviewsRouter, prefix='/api')
app.include_router(UsersRouter, prefix='/api')

@app.get('/')
def home():
  return {'message': 'Home Page'}


