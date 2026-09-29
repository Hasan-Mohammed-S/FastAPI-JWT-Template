from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# Associations
from .review import ReviewModel
from .user import UserModel
from .base import BaseModel

#  MovieModel extends SQLAlchemy's Base class.
#  Extending Base lets SQLAlchemy 'know' about our model, so it can use it.

class MovieModel(BaseModel):

    def __str__(self):
        return f"{self.id}: {self.name}"

    # This will be used directly to make a
    # TABLE in Postgresql
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)

    # Specific columns for our Movie Table.
    name = Column(String, unique=True)
    in_stock = Column(Boolean)
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Associations
    user = relationship("UserModel", back_populates="movies")
    reviews = relationship('ReviewsModel', back_populates="movie")