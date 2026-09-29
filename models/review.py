from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

#  ReviewsModel extends SQLAlchemy's Base class.
#  Extending Base lets SQLAlchemy 'know' about our model, so it can use it.

class ReviewModel(BaseModel):

    # This will be used directly to make a
    # TABLE in Postgresql
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    # Specific columns for our Reviews Table.
    content = Column(String, nullable=False)

    # Associations:
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    movie = relationship('MovieModel', back_populates="reviews")