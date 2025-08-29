"""
Ce fichier contiendra le ou les modèles de personnes qui serviront à alimenter les algoritmes
de calcul.
"""


class Personne:
    def __init__(self, nom: str, prenom: str, age: int, sexe: str,
                 profession: str, salaire: float, age_limite: int,
                 situation_matrimoniale: str, conjoints: list, enfants: list,
                 ascendants: list, collateraux: list,
                 pays_residence: str, pays_sinistre: str):

        # Relativement à son acte de naissance
        self.nom: str = nom
        self.prenom: str = prenom
        self.age: int = age
        self.sexe: str = sexe

        # Relativement à sa vie professionnelle
        self.profession: str = profession
        self.salaire: float = salaire
        self.age_limite: int = age_limite

        # Relativement à sa vie conjuguale (en cas de décès pour les ayants droit)
        self.situation_matrimoniale: str = situation_matrimoniale
        self.conjoints: list[Conjoint] = conjoints # {"conjoin_1": ("nom", "prenom", "âge"), ...}
        self.enfants: list[Enfant] = enfants # Ce sont les descendants, # (enfant_1, enfant_2, ...)

        # Relativement à son entourage familial
        self.ascendants: list[Ascendant] = ascendants # (enfant_1, enfant_2, ...)
        self.collateraux: list[Collateral] = collateraux # {"collateral_1": ("nom", "prenom", "âge"), ...}

        # Relativement à l'appréciation du SMIG à retenir
        self.pays_residence: str = pays_residence
        self.pays_sinistre: str = pays_sinistre
    pass


class Enfant:
    def __init__(self, nom: str, prenom: str, age: int, sexe="M",
                 handicap_majeur: bool = False, orphelin_double: bool = False, poursuit_etudes: bool = True,):
        self.nom: str = nom
        self.prenom: str = prenom
        self.sexe: str = sexe # Ou F pour féminin.
        self.age: int = age
        self.handicap_majeur: bool = handicap_majeur # Pour le cas de certains enfants qui sont amenés à être toute
        # leur vie durant à la charge de leurs parents, l'indemnisation preend un aspect viager.
        self.orphelin_double = orphelin_double # True si Oui, False si Non.
        self.poursuit_etudes: bool = poursuit_etudes

        self.prejudice_economique: float = 0.0 # Pour le préjudice économique de l'enfant.
        self.prejudice_moral: float = 0.0 # Pour le préjudice moral de l'enfant.
        self.proportion: float = 0.0  # Cet attribut servira dans la répartion des indemnités au regard des plafonds fixé par le code CIMA.
        pass
    pass


class Conjoint:
    def __init__(self, nom: str, prenom: str, age: int, sexe: str = "F"):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.sexe = sexe

        self.prejudice_economique: float = 0.0  # Pour le préjudice économique du conjoint.
        self.prejudice_moral: float = 0.0  # Pour le préjudice moral du conjoint.
        self.proportion: float = 0.0 # Cet attribut servira dans la répartion des indemnités au regard des plafonds fixé par le code CIMA.
    pass


class Ascendant:
    def __init__(self, nom, prenom, age, sexe):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.sexe = sexe

        self.prejudice_economique: float = 0.0  # Pour le préjudice économique du conjoint.
        self.prejudice_moral: float = 0.0  # Pour le préjudice moral du conjoint.
        self.proportion: float = 0.0  # Cet attribut servira dans la répartion des indemnités au regard des plafonds fixé par le code CIMA.
    pass


class Collateral:
    def __init__(self, nom: str, prenom: str, age: int):
        self.nom = nom
        self.prenom = prenom
        self.age = age

        self.prejudice_economique: float = 0.0  # Pour le préjudice économique du conjoint.
        self.prejudice_moral: float = 0.0  # Pour le préjudice moral du conjoint.
        self.proportion: float = 0.0  # Cet attribut servira dans la répartion des indemnités au regard des plafonds fixé par le code CIMA.
    pass
