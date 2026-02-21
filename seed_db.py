import os
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models.candidato_model import Candidato
from src.models.voting_location_model import VotingLocation

def seed_database():
    # Asegurar que las tablas existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar si ya existe la ubicación de votación
        location = db.query(VotingLocation).first()
        if not location:
            # Coordenadas aproximadas de la Universidad Continental (Sede Huancayo o principal)
            print("Seeding Voting Location...")
            new_location = VotingLocation(
                name="Campus Universidad Continental",
                latitude=-12.047280,  # Reemplazar con coords correctas si es necesario
                longitude=-75.199052,
                radius_meters=100.0
            )
            db.add(new_location)
            db.commit()

        # Verificar si ya hay candidatos
        candidates_count = db.query(Candidato).count()
        if candidates_count == 0:
            print("Seeding Candidates...")
            candidatos_iniciales = [
                Candidato(
                    nombre="Juan Pérez",
                    foto_url="https://ui-avatars.com/api/?name=Juan+Perez&background=0D8ABC&color=fff",
                    propuesta="Mejora en los laboratorios de cómputo y licencias de software libre.",
                    role="DELEGADO"
                ),
                Candidato(
                    nombre="María Gómez",
                    foto_url="https://ui-avatars.com/api/?name=Maria+Gomez&background=F0AB00&color=fff",
                    propuesta="Mayor integración deportiva y eventos culturales.",
                    role="DELEGADO"
                ),
                Candidato(
                    nombre="Carlos López",
                    foto_url="https://ui-avatars.com/api/?name=Carlos+Lopez&background=2E86C1&color=fff",
                    propuesta="Tutorías entre estudiantes para cursos de programación y matemáticas.",
                    role="SUBDELEGADO"
                )
            ]
            db.bulk_save_objects(candidatos_iniciales)
            db.commit()
            print("Seed completado exitosamente.")
        else:
            print("La base de datos ya contiene candidatos. Omitiendo seed de candidatos.")

    except Exception as e:
        import traceback
        print(f"Error seeding database:")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
