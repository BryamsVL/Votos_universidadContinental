from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, Float
from sqlalchemy.sql import func
from src.database import Base


class Voto(Base):
    __tablename__ = "votos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    candidato_id = Column(Integer, ForeignKey("candidatos.id"), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint("usuario_id", name="uq_voto_usuario"),
    )
