from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

# Read Only
Base = declarative_base()

class Visibility(enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    bio = Column(String)
    profile_image = Column(String)
    # TODO: age
    # TODO: gender
    # TODO: favorite_workout_type

    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Feed(Base):
    __tablename__ = "feeds"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)
    content = Column(String)
    visibility = Column(Enum(Visibility))
    image = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # TODO: location
