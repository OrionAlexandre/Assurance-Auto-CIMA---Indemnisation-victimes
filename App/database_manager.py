from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, joinedload
from sqlalchemy.ext.associationproxy import association_proxy

from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Union, Type

from api import default_personne
#=======================================================================================================================
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

    # Relation avec Personne
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

    # Relation avec Personne
    personne_id = Column(Integer, ForeignKey('personnes.id'))
    personne = relationship("Personne", back_populates="conjoints")


class Ascendant(Base):
    __tablename__ = 'ascendants'

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    sexe = Column(String(1), nullable=False)
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

    # Relations
    conjoints = relationship("Conjoint", back_populates="personne", cascade="all, delete-orphan")
    enfants = relationship("Enfant", back_populates="personne", cascade="all, delete-orphan")
    ascendants = relationship("Ascendant", back_populates="personne", cascade="all, delete-orphan")
    collateraux = relationship("Collateral", back_populates="personne", cascade="all, delete-orphan")


engine = create_engine('sqlite:///assurance.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def personnes() -> list:
    session = Session()
    try:
        personnes = session.query(Personne).all()
        return personnes
    finally:
        session.close()


def ajouter_personne_data_base(personne_instance: Personne) -> Personne:
    """
    Ajoute une instance de Personne à la base de données

    Args:
        personne_instance: Instance de la classe Personne avec tous ses ayants droit

    Returns:
        Personne: L'objet personne créé avec son ID
    """
    session = Session()
    try:

        """
        # Vérification que l'instance est de type Personne
        if not isinstance(personne_instance, Personne):
            raise TypeError("L'argument doit être une instance de Personne")
        
        # Vérification que l'instance n'a pas déjà un ID (déjà en base)
        if personne_instance.id is not None:
            raise ValueError("Cette personne est déjà en base de données")
        """

        # Ajout à la session et commit
        session.add(personne_instance)
        session.commit()

        # print(f"✅ Personne ajoutée avec ID: {personne_instance.id}")
        return personne_instance

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur lors de l'ajout: {e}")
        raise
    finally:
        session.close()


def rechercher_personne_par_id(personne_id) -> Personne | None:
    session = Session()
    try:
        personne = session.query(Personne).options(
                joinedload(Personne.enfants),
                joinedload(Personne.conjoints),
                joinedload(Personne.ascendants),
                joinedload(Personne.collateraux)
            ).filter(Personne.id == personne_id).first()
        return personne
    finally:
        session.close()


def rechercher_ayants_droits_par_id(
        personne_id: int,
        table_type: str = "enfants"
) -> Union[List[Enfant], List[Conjoint], List[Ascendant], List[Collateral], None]:
    # Mapping des types de table aux classes
    table_mapping = {
        "enfants": Enfant,
        "conjoints": Conjoint,
        "ascendants": Ascendant,
        "collateraux": Collateral
    }

    # Validation du type de table
    table_type_lower = table_type.lower()
    if table_type_lower not in table_mapping:
        raise ValueError(f"Type de table invalide: {table_type}. Options valides: {list(table_mapping.keys())}")

    table_class = table_mapping[table_type_lower]

    session = Session()
    try:
        ayants_droits = session.query(table_class) \
            .filter(table_class.personne_id == personne_id) \
            .all()
        return ayants_droits if ayants_droits else None
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")
        return None
    finally:
        session.close()


def supprimer_et_reorganiser_ids(personne_id) -> bool:
    session = Session()
    try:
        # 1. Vérifier si la personne existe
        personne = session.query(Personne).filter(Personne.id == personne_id).first()
        if not personne:
            print(f"Personne avec ID {personne_id} non trouvée")
            return False

        # 2. Supprimer la personne (cascade supprimera automatiquement les ayants droit)
        session.delete(personne)
        session.flush()  # Applique la suppression sans commit

        # 3. Réorganiser toutes les tables
        tables = [Personne, Enfant, Conjoint, Ascendant, Collateral]

        for table in tables:
            # Récupérer tous les enregistrements triés par ID
            records = session.query(table).order_by(table.id).all()

            # Réassigner les IDs séquentiellement
            nouvel_id = 1
            for record in records:
                if record.id != nouvel_id:
                    # Sauvegarder l'ancien ID
                    ancien_id = record.id

                    # Mettre à jour l'ID
                    record.id = nouvel_id

                    # Si c'est une table d'ayants droit, mettre à jour la référence personne_id
                    if hasattr(record, 'personne_id') and record.personne_id:
                        # Trouver le nouvel ID de la personne référencée
                        personne_ref = session.query(Personne).filter(Personne.id == record.personne_id).first()
                        if personne_ref:
                            record.personne_id = personne_ref.id

                nouvel_id += 1

        # 4. Valider tous les changements
        session.commit()
        print(f"Personne {personne_id} supprimée et IDs réorganisés avec succès")
        return True

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression et réorganisation: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()


if __name__ == '__main__':
    # Initialisation de la base de données
    engine = create_engine('sqlite:///assurance.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

