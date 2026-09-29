from fastapi import APIRouter, Depends, HTTPException

# Models
from models.movie import MovieModel

# Serializers & Validations
from serializers.movie import MovieSchema, CreateMovieSchema, UpdateMovieSchema
from serializers.user import UserSchema
from typing import List

# DB
from sqlalchemy.orm import Session
from database import get_db

# Dependencies
from dependencies.get_current_user import get_current_user


router = APIRouter()

@router.get('/movies', response_model=List[MovieSchema])
def get_movies(db: Session = Depends(get_db)):
  movies = db.query(MovieModel).all()

  return movies

@router.get("/movies/{movie_id}", response_model=MovieSchema)
def get_single_movie(movie_id: int, db: Session = Depends(get_db)):
  movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

  if not movie:
    raise HTTPException(status_code=404, detail="Cannot find Movie")

  return movie


@router.post("/movies", response_model=MovieSchema, status_code=201)
def create_movie(movie: CreateMovieSchema, db: Session = Depends(get_db), user: UserSchema = Depends(get_current_user)):
    try:
      new_movie = MovieModel(**movie.dict(), user_id = user.id)# Convert Pydantic model to SQLAlchemy model
      db.add(new_movie)
      db.commit() # basicallt model.save()
      db.refresh(new_movie)

    except:
       raise HTTPException(status_code=422, detail="Unprocessable Entity")

    return new_movie



@router.put("/movies/{movie_id}", response_model=MovieSchema)
def update_movie(
   movie_id: int,
   movie: UpdateMovieSchema,
   db: Session = Depends(get_db),
   user: UserSchema = Depends(get_current_user)
   ):

    # Find the movie to update
    db_movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    # If movie was not found, raise an error
    if not db_movie:
      raise HTTPException(status_code=404, detail="Movie not found")

    if db_movie.user_id != user.id: # type: ignore
      raise HTTPException(status_code=403, detail="Forbidden")

    movie_data = movie.dict(exclude_unset=True)

    # loop thru the dict and replace the value for the key
    for key, value in movie_data.items():
       setattr(db_movie, key, value)

    db.commit()
    db.refresh(db_movie)

    return db_movie

@router.delete("/movies/{movie_id}", status_code=204)
def delete_movie(
   movie_id: int,
   db: Session = Depends(get_db),
   user: UserSchema = Depends(get_current_user)
  ):
    # Delete a movie by ID
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    # If movie was not found, raise an error
    if not movie:
      raise HTTPException(status_code=404, detail="Movie not found")

    if movie.user_id != user.id: # type: ignore
      raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(movie)
    db.commit()

    return None
    # return {"message": f"Movie with ID {movie_id} has been deleted"}