from sqlalchemy import Column, Integer, String, Text
from src.database import Base


class Candidato(Base):
    __tablename__ = "candidatos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    propuesta = Column(Text, nullable=True)
    foto_url = Column(Text, nullable=True)
    role = Column(String, nullable=True)  # 'delegado' o 'subdelegado'
