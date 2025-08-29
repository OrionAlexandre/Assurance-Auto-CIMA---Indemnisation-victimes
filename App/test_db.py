from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from faker import Faker
import random

from algorithm.tables import SituationMatrimoniale

# Initialisation de Faker pour générer des données réalistes
fake = Faker('fr_FR')

Base = declarative_base()



class Enfant(Base):
    __tablename__ = 'enfants'

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    sexe = Column(String(1), nullable=False)
    handicap_majeur = Column(Boolean, default=False)
    orphelin_double = Column(Boolean, default=False)
    poursuit_etudes = Column(Boolean, default=True)
    prejudice_economique = Column(Float, default=0.0)
    prejudice_moral = Column(Float, default=0.0)
    proportion = Column(Float, default=0.0)

    personne_id = Column(Integer, ForeignKey('personnes.id'))
    personne = relationship("Personne", back_populates="enfants")


class Conjoint(Base):
    __tablename__ = 'conjoints'

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    sexe = Column(String(1), default="F")
    prejudice_economique = Column(Float, default=0.0)
    prejudice_moral = Column(Float, default=0.0)
    proportion = Column(Float, default=0.0)

    personne_id = Column(Integer, ForeignKey('personnes.id'))
    personne = relationship("Personne", back_populates="conjoints")


class Ascendant(Base):
    __tablename__ = 'ascendants'

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    sexe = Column(String(1), default="F")
    prejudice_economique = Column(Float, default=0.0)
    prejudice_moral = Column(Float, default=0.0)
    proportion = Column(Float, default=0.0)

    personne_id = Column(Integer, ForeignKey('personnes.id'))
    personne = relationship("Personne", back_populates="ascendants")


class Collateral(Base):
    __tablename__ = 'collateraux'

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    prejudice_economique = Column(Float, default=0.0)
    prejudice_moral = Column(Float, default=0.0)
    proportion = Column(Float, default=0.0)

    personne_id = Column(Integer, ForeignKey('personnes.id'))
    personne = relationship("Personne", back_populates="collateraux")


class Personne(Base):
    __tablename__ = 'personnes'

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    sexe = Column(String(1), nullable=False)
    profession = Column(String, nullable=False)
    salaire = Column(Float, nullable=False)
    age_limite = Column(Integer, nullable=False)
    situation_matrimoniale = Column(String, nullable=False)
    pays_residence = Column(String, nullable=False)
    pays_sinistre = Column(String, nullable=False)

    conjoints = relationship("Conjoint", back_populates="personne", cascade="all, delete-orphan")
    enfants = relationship("Enfant", back_populates="personne", cascade="all, delete-orphan")
    ascendants = relationship("Ascendant", back_populates="personne", cascade="all, delete-orphan")
    collateraux = relationship("Collateral", back_populates="personne", cascade="all, delete-orphan")


# Initialisation de la base de données
engine = create_engine('sqlite:///assurance.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Fonction pour rechercher une personne par ID
def rechercher_personne_par_id(personne_id) -> Personne | None:
    session = Session()
    try:
        personne = session.query(Personne).filter(Personne.id == personne_id).first()
        return personne
    finally:
        session.close()


# Fonctions de recherche existantes
def rechercher_personnes_par_nom(nom) -> list:
    session = Session()
    try:
        result = session.query(Personne).filter(Personne.nom == nom).all()
        return result
    finally:
        session.close()


# Création de données de test réalistes
def creer_donnees_test_realistes():
    session = Session()

    # Création de 10 profils enfants
    enfants = []
    for i in range(10):
        sexe = random.choice(['M', 'F'])
        enfant = Enfant(
            nom=fake.last_name(),
            prenom=fake.first_name_male() if sexe == 'M' else fake.first_name_female(),
            age=random.randint(0, 25),
            sexe=sexe,
            handicap_majeur=random.choice([True, False, False, False]),  # 25% de chance
            orphelin_double=random.choice([True, False, False, False, False]),  # 20% de chance
            poursuit_etudes=random.choice([True, True, True, False])  # 75% de chance
        )
        enfants.append(enfant)
        session.add(enfant)

    # Création de 13 profils conjoints
    conjoints = []
    for i in range(13):
        sexe = random.choice(['M', 'F'])
        conjoint = Conjoint(
            nom=fake.last_name(),
            prenom=fake.first_name_male() if sexe == 'M' else fake.first_name_female(),
            age=random.randint(25, 80),
            sexe=sexe
        )
        conjoints.append(conjoint)
        session.add(conjoint)

    # Création de 7 profils ascendants (parents, grands-parents)
    ascendants = []
    for i in range(7):
        ascendant = Ascendant(
            nom=fake.last_name(),
            prenom=fake.first_name(),
            age=random.randint(60, 95),
            sexe = random.choice(['M', 'F'])
        )
        ascendants.append(ascendant)
        session.add(ascendant)

    # Création de 5 profils collatéraux (frères, sœurs, oncles, tantes)
    collateraux = []
    for i in range(5):
        collateral = Collateral(
            nom=fake.last_name(),
            prenom=fake.first_name(),
            age=random.randint(18, 70)
        )
        collateraux.append(collateral)
        session.add(collateral)

    # Création de 12 profils personnes principales
    professions = ["Ingénieur", "Médecin", "Enseignant", "Commerçant", "Agriculteur",
                   "Fonctionnaire", "Artisan", "Cadre", "Ouvrier", "Retraité"]

    pays = ["Congo", "Togo", "Cameroun", "Gabon", "Sénégal", "Côte d'Ivoire"]

    personnes = []
    for i in range(12):
        sexe = random.choice(['M', 'F'])
        situation = random.choice([SituationMatrimoniale.CELIBATAIRE,
                                    SituationMatrimoniale.MARIE_E,
                                    SituationMatrimoniale.DIVORCE,
                                    SituationMatrimoniale.VEUF_VE])

        personne = Personne(
            nom=fake.last_name(),
            prenom=fake.first_name_male() if sexe == 'M' else fake.first_name_female(),
            age=random.randint(25, 65),
            sexe=sexe,
            profession=random.choice(professions),
            salaire=random.randint(50000, 500000),
            age_limite=random.randint(60, 70),
            situation_matrimoniale=situation,
            pays_residence=random.choice(pays),
            pays_sinistre=random.choice(pays)
        )

        # Répartition réaliste des entourages
        if situation in [SituationMatrimoniale.MARIE_E, SituationMatrimoniale.VEUF_VE]:
            # 1-2 conjoints pour les personnes mariées/veuves
            num_conjoints = random.randint(1, 2) if situation == SituationMatrimoniale.MARIE_E else 1
            personne.conjoints.extend(random.sample(conjoints, min(num_conjoints, len(conjoints))))

        # Enfants (0-4 enfants par personne)
        num_enfants = random.randint(0, 4)
        personne.enfants.extend(random.sample(enfants, min(num_enfants, len(enfants))))

        # Ascendants (0-2 par personne, plus probable pour les jeunes)
        if personne.age < 40:
            num_ascendants = random.choices([0, 1, 2], weights=[0.2, 0.5, 0.3])[0]
        else:
            num_ascendants = random.choices([0, 1], weights=[0.7, 0.3])[0]
        personne.ascendants.extend(random.sample(ascendants, min(num_ascendants, len(ascendants))))

        # Collatéraux (0-3 par personne)
        num_collateraux = random.randint(0, 3)
        personne.collateraux.extend(random.sample(collateraux, min(num_collateraux, len(collateraux))))

        personnes.append(personne)
        session.add(personne)

    session.commit()
    session.close()
    print("Données de test réalistes créées avec succès!")


# Exemple d'utilisation
if __name__ == "__main__":
    # Créer les données de test
    creer_donnees_test_realistes()

    # Tester la recherche par ID
    personne = rechercher_personne_par_id(1)
    if personne:
        print(f"Personne trouvée: {personne.prenom} {personne.nom}")

    # Rechercher par nom
    personnes_dupont = rechercher_personnes_par_nom("Dupont")
    print(f"Nombre de personnes Dupont trouvées: {len(personnes_dupont)}")