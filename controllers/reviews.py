from fastapi import APIRouter, Depends, HTTPException

# Models
from models.movie import MovieModel
from models.review import ReviewModel

# Serializers & Validations
from serializers.review import ReviewSchema, CreateReviewSchema, UpdateReviewSchema
from typing import List

# DB
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.get("/movies/{movie_id}/reviews", response_model=List[ReviewSchema])
def get_reviews_for_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie.reviews

@router.get("/reviews/{review_id}", response_model=ReviewSchema)
def get_review_by_id(review_id: int,  db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()

    if not review:
            raise HTTPException(status_code=404, detail="review not found")

    return reviews

@router.post("/movie/{movie_id}/reviews", response_model=ReviewSchema, status_code=201)
def create_review(movie_id: int, review: CreateReviewSchema, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    new_review = ReviewModel(**review.dict(), movie_id=movie_id)

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review

@router.put("/reviews/{review_id}", response_model=ReviewSchema)
def update_review(review_id: int, review: UpdateRreviewSchema, db: Session = Depends(get_db)):
  db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()

  if not db_review:
    raise HTTPException(status_code=404, detail="Review not found")

  review_data = review.dict(exclude_unset=True)

  for key, val in review_data.items():
      setattr(db_review, key, val)

  db.commit()
  db.refresh(db_review)

  return db_reviewt

@router.delete("/reviews/{review_id}", status_code=204)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()

    if not db_review:
      raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()

    return None

