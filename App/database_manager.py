from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, joinedload, make_transient
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import text

from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Union, Type

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
        # return personne_instance

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

from sqlalchemy.orm import joinedload


def supprimer_personne(personne_id: int) -> bool:
    session = Session()
    try:
        # Charger la personne avec tous ses ayants droit
        personne = session.query(Personne).options(
            joinedload(Personne.enfants),
            joinedload(Personne.conjoints),
            joinedload(Personne.ascendants),
            joinedload(Personne.collateraux)
        ).filter(Personne.id == personne_id).first()

        if not personne:
            print("❌ Personne introuvable")
            return False

        session.delete(personne)
        session.commit()
        print(f"✅ Personne {personne_id} et ses ayants droit supprimés")
        return True

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur: {e}")
        return False
    finally:
        session.close()


def supprimer_ayants_droits(personne_id: int) -> bool:
    """
    Supprime tous les ayants droits (enfants, conjoints, ascendants, collatéraux)
    d'une personne sans supprimer la personne elle-même.

    Args:
        personne_id: ID de la personne dont on veut supprimer les ayants droits

    Returns:
        bool: True si succès, False si échec
    """
    session = Session()
    try:
        # Vérifier que la personne existe
        personne = session.query(Personne).filter(Personne.id == personne_id).first()
        if not personne:
            print(f"❌ Personne avec ID {personne_id} non trouvée")
            return False

        # Compter le nombre d'ayants droit avant suppression
        compteur_avant = {
            'enfants': session.query(Enfant).filter(Enfant.personne_id == personne_id).count(),
            'conjoints': session.query(Conjoint).filter(Conjoint.personne_id == personne_id).count(),
            'ascendants': session.query(Ascendant).filter(Ascendant.personne_id == personne_id).count(),
            'collateraux': session.query(Collateral).filter(Collateral.personne_id == personne_id).count()
        }

        print(f"Suppression des ayants droits pour la personne ID {personne_id}...")
        print(f"Avant suppression - Enfants: {compteur_avant['enfants']}, "
              f"Conjoints: {compteur_avant['conjoints']}, "
              f"Ascendants: {compteur_avant['ascendants']}, "
              f"Collatéraux: {compteur_avant['collateraux']}")

        # Supprimer tous les ayants droit
        tables_ayants = [Enfant, Conjoint, Ascendant, Collateral]
        resultats = {}

        for table in tables_ayants:
            resultat = session.query(table).filter(table.personne_id == personne_id).delete()
            resultats[table.__tablename__] = resultat
            print(f"  ✅ {table.__tablename__}: {resultat} élément(s) supprimé(s)")

        session.commit()

        # Vérification après suppression
        compteur_apres = {
            'enfants': session.query(Enfant).filter(Enfant.personne_id == personne_id).count(),
            'conjoints': session.query(Conjoint).filter(Conjoint.personne_id == personne_id).count(),
            'ascendants': session.query(Ascendant).filter(Ascendant.personne_id == personne_id).count(),
            'collateraux': session.query(Collateral).filter(Collateral.personne_id == personne_id).count()
        }

        print(f"Après suppression - Enfants: {compteur_apres['enfants']}, "
              f"Conjoints: {compteur_apres['conjoints']}, "
              f"Ascendants: {compteur_apres['ascendants']}, "
              f"Collatéraux: {compteur_apres['collateraux']}")

        print(f"✅ Tous les ayants droits de la personne ID {personne_id} ont été supprimés")
        return True

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur lors de la suppression des ayants droits: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()


def reorganiser_base_completement() -> bool:
    """
    Sauvegarde toutes les personnes avec leurs ayants droits, vide la base,
    puis réinsère tout avec des IDs séquentiels tout en préservant les relations.
    """
    session = Session()
    try:
        print("🔃 Début de la réorganisation complète de la base...")

        # 1. Sauvegarder TOUTES les données avec leurs relations
        print("💾 Sauvegarde de toutes les données...")
        personnes_completes = session.query(Personne).options(
            joinedload(Personne.enfants),
            joinedload(Personne.conjoints),
            joinedload(Personne.ascendants),
            joinedload(Personne.collateraux)
        ).order_by(Personne.id).all()

        # Créer une structure de sauvegarde
        sauvegarde = []
        for personne in personnes_completes:
            personne_data = {
                'ancien_id': personne.id,
                'nom': personne.nom,
                'prenom': personne.prenom,
                'age': personne.age,
                'sexe': personne.sexe,
                'profession': personne.profession,
                'salaire': personne.salaire,
                'age_limite': personne.age_limite,
                'situation_matrimoniale': personne.situation_matrimoniale,
                'pays_residence': personne.pays_residence,
                'pays_sinistre': personne.pays_sinistre,
                'enfants': [],
                'conjoints': [],
                'ascendants': [],
                'collateraux': []
            }

            # Sauvegarder les enfants
            for enfant in personne.enfants:
                personne_data['enfants'].append({
                    'nom': enfant.nom,
                    'prenom': enfant.prenom,
                    'age': enfant.age,
                    'sexe': enfant.sexe,
                    'handicap_majeur': enfant.handicap_majeur,
                    'orphelin_double': enfant.orphelin_double,
                    'poursuit_etudes': enfant.poursuit_etudes,
                    'prejudice_economique': enfant.prejudice_economique,
                    'prejudice_moral': enfant.prejudice_moral,
                    'proportion': enfant.proportion
                })

            # Sauvegarder les conjoints
            for conjoint in personne.conjoints:
                personne_data['conjoints'].append({
                    'nom': conjoint.nom,
                    'prenom': conjoint.prenom,
                    'age': conjoint.age,
                    'sexe': conjoint.sexe,
                    'prejudice_economique': conjoint.prejudice_economique,
                    'prejudice_moral': conjoint.prejudice_moral,
                    'proportion': conjoint.proportion
                })

            # Sauvegarder les ascendants
            for ascendant in personne.ascendants:
                personne_data['ascendants'].append({
                    'nom': ascendant.nom,
                    'prenom': ascendant.prenom,
                    'age': ascendant.age,
                    'sexe': ascendant.sexe,
                    'prejudice_economique': ascendant.prejudice_economique,
                    'prejudice_moral': ascendant.prejudice_moral,
                    'proportion': ascendant.proportion
                })

            # Sauvegarder les collatéraux
            for collateral in personne.collateraux:
                personne_data['collateraux'].append({
                    'nom': collateral.nom,
                    'prenom': collateral.prenom,
                    'age': collateral.age,
                    'prejudice_economique': collateral.prejudice_economique,
                    'prejudice_moral': collateral.prejudice_moral,
                    'proportion': collateral.proportion
                })

            sauvegarde.append(personne_data)

        print(f"✅ {len(sauvegarde)} personnes sauvegardées avec leurs ayants droits")

        # 2. VIDER COMPLÈTEMENT la base de données
        print("🗑️  Vidage de la base de données...")

        # Désactiver les contraintes foreign key
        session.execute(text("PRAGMA foreign_keys=OFF"))

        # Vider dans l'ordre inverse des relations (d'abord les ayants droit)
        tables = [Enfant, Conjoint, Ascendant, Collateral, Personne]
        for table in tables:
            deleted_count = session.query(table).delete()
            print(f"  ✅ {table.__tablename__}: {deleted_count} élément(s) supprimé(s)")

        session.commit()

        # 3. RÉINSÉRER toutes les données avec de nouveaux IDs séquentiels
        print("🔄 Réinsertion avec nouveaux IDs...")

        mapping_anciens_ids = {}  # ancien_id -> nouvel_id

        for nouvel_id, personne_data in enumerate(sauvegarde, start=1):
            # Créer la nouvelle personne avec nouvel ID
            nouvelle_personne = Personne(
                id=nouvel_id,
                nom=personne_data['nom'],
                prenom=personne_data['prenom'],
                age=personne_data['age'],
                sexe=personne_data['sexe'],
                profession=personne_data['profession'],
                salaire=personne_data['salaire'],
                age_limite=personne_data['age_limite'],
                situation_matrimoniale=personne_data['situation_matrimoniale'],
                pays_residence=personne_data['pays_residence'],
                pays_sinistre=personne_data['pays_sinistre']
            )

            session.add(nouvelle_personne)
            session.flush()  # Pour s'assurer que l'ID est bien attribué

            # Stocker le mapping d'ID
            mapping_anciens_ids[personne_data['ancien_id']] = nouvel_id

            # Réinsérer les enfants
            for enfant_data in personne_data['enfants']:
                enfant = Enfant(
                    nom=enfant_data['nom'],
                    prenom=enfant_data['prenom'],
                    age=enfant_data['age'],
                    sexe=enfant_data['sexe'],
                    handicap_majeur=enfant_data['handicap_majeur'],
                    orphelin_double=enfant_data['orphelin_double'],
                    poursuit_etudes=enfant_data['poursuit_etudes'],
                    prejudice_economique=enfant_data['prejudice_economique'],
                    prejudice_moral=enfant_data['prejudice_moral'],
                    proportion=enfant_data['proportion'],
                    personne_id=nouvel_id  # ⚠️ Référence correcte vers le nouvel ID
                )
                session.add(enfant)

            # Réinsérer les conjoints
            for conjoint_data in personne_data['conjoints']:
                conjoint = Conjoint(
                    nom=conjoint_data['nom'],
                    prenom=conjoint_data['prenom'],
                    age=conjoint_data['age'],
                    sexe=conjoint_data['sexe'],
                    prejudice_economique=conjoint_data['prejudice_economique'],
                    prejudice_moral=conjoint_data['prejudice_moral'],
                    proportion=conjoint_data['proportion'],
                    personne_id=nouvel_id  # ⚠️ Référence correcte
                )
                session.add(conjoint)

            # Réinsérer les ascendants
            for ascendant_data in personne_data['ascendants']:
                ascendant = Ascendant(
                    nom=ascendant_data['nom'],
                    prenom=ascendant_data['prenom'],
                    age=ascendant_data['age'],
                    sexe=ascendant_data['sexe'],
                    prejudice_economique=ascendant_data['prejudice_economique'],
                    prejudice_moral=ascendant_data['prejudice_moral'],
                    proportion=ascendant_data['proportion'],
                    personne_id=nouvel_id  # ⚠️ Référence correcte
                )
                session.add(ascendant)

            # Réinsérer les collatéraux
            for collateral_data in personne_data['collateraux']:
                collateral = Collateral(
                    nom=collateral_data['nom'],
                    prenom=collateral_data['prenom'],
                    age=collateral_data['age'],
                    prejudice_economique=collateral_data['prejudice_economique'],
                    prejudice_moral=collateral_data['prejudice_moral'],
                    proportion=collateral_data['proportion'],
                    personne_id=nouvel_id  # ⚠️ Référence correcte
                )
                session.add(collateral)

        # Réactiver les contraintes et commit final
        session.execute(text("PRAGMA foreign_keys=ON"))
        session.commit()

        print(f"✅ Réorganisation terminée avec succès!")
        print(f"   {len(sauvegarde)} personnes réinsérées")
        print(f"   IDs séquentiels: 1 à {len(sauvegarde)}")

        return True

    except Exception as e:
        session.rollback()
        session.execute(text("PRAGMA foreign_keys=ON"))  # Réactiver en cas d'erreur
        print(f"❌ Erreur lors de la réorganisation: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()


def supprimer_et_reorganiser_ids(personne_id):
    supprimer_ayants_droits(personne_id)
    supprimer_personne(personne_id)
    reorganiser_base_completement()
    pass


if __name__ == '__main__':
    # Initialisation de la base de données
    engine = create_engine('sqlite:///assurance.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

