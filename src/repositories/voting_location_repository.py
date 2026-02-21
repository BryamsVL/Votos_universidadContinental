from sqlalchemy.orm import Session
from src.models.voting_location_model import VotingLocation


def get_all(db: Session) -> list[VotingLocation]:
    return db.query(VotingLocation).all()
