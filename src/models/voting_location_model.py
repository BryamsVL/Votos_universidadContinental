from sqlalchemy import Column, Integer, String, Float
from src.database import Base


class VotingLocation(Base):
    __tablename__ = "voting_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius_meters = Column(Float, nullable=False, default=100.0)
