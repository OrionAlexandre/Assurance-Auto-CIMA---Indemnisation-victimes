from algorithm.dead import PrejudiceEconomiqueConjoints, PrejudiceEconomiqueAscendants, ControlePlafondPrejudiceEconomique, PrejudiceEconomiqueEnfants,\
    PrejudiceMoral, ControlePlafondPrejudiceMoral
from algorithm.profils import Enfant, Conjoint, Personne

from algorithm.tables import SituationMatrimoniale, smig_pays_cima_2025

import logging
import os
from pathlib import Path


class ErrorLogger:
    def __init__(self, log_file="error.log"):
        self.log_file = log_file
        self._setup_logger()

    def _setup_logger(self):
        """Configure le système de logging"""
        # Créer le dossier s'il n'existe pas
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Configuration du logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            encoding='utf-8'
        )

    def log_error(self, message: str, exception: Exception = None):
        """
        Écrit un message d'erreur dans le fichier log

        Args:
            message: Description de l'erreur
            exception: Exception à logger (optionnel)
        """
        try:
            if exception:
                logging.error(f"{message} - Exception: {exception}", exc_info=True)
            else:
                logging.error(message)

            print(f"✅ Erreur loggée: {message}")
        except Exception as e:
            print(f"❌ Erreur lors de l'écriture du log: {e}")

    def log_warning(self, message: str):
        """Écrit un avertissement"""
        logging.warning(message)

    def log_info(self, message: str):
        """Écrit un message d'information"""
        logging.info(message)

    def clear_log(self):
        """Vide le fichier log"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")
            print("📋 Fichier log vidé")
        except Exception as e:
            print(f"❌ Erreur vidage log: {e}")

    def read_log(self):
        """Lit et retourne le contenu du fichier log"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return f.read()
            return "Aucun fichier log trouvé"
        except Exception as e:
            return f"Erreur lecture log: {e}"


# Instance globale pour un usage facile
error_logger = ErrorLogger()

#=======================================================================================================================
jean_pascal = Enfant(
            nom="TEST",
            prenom="Jean Pascal",
            age=12,
            sexe="M",
            handicap_majeur=True,
            orphelin_double=True
        )
jean_lucien = Enfant(
            nom="TEST",
            prenom="Jean Lucien",
            age=18,
            sexe="M",
            handicap_majeur=False,
            orphelin_double=True
        )
rosalie = Enfant(
            nom="TEST",
            prenom="Rosalie",
            age=23,
            sexe="F",
            handicap_majeur=False,
        )
rene = Enfant(
    nom="TEST",
    prenom="René",
    age=15,
    sexe="M",
    handicap_majeur=False,
)
marie = Conjoint(
    nom="TEST",
    prenom="Marie",
    age=35,
    sexe="F",
)
germaine = Conjoint(
    nom="TEST",
    prenom="Germaine",
    age=40,
    sexe="F",
)
default_personne = Personne(
    nom="TEST",
    prenom="Test",
    age=23,
    sexe="M",
    profession="Profession test",
    salaire=445000,
    age_limite=60,
    situation_matrimoniale=SituationMatrimoniale.CELIBATAIRE,
    conjoints=[marie, germaine],
    enfants=[rosalie, rene, jean_pascal, jean_lucien],
    ascendants=[],
    collateraux=[],
    pays_residence="Togo",
    pays_sinistre="Togo",
)


def save_default_personne_alive(personne):
    import pickle
    print("Sauvegade d'une victime alive...")
    with open("default_personne_alive.pkl", "wb") as fichier:
        pickle.dump(personne, fichier)


def laod_default_personne_alive():
    import pickle
    with open("default_personne_alive.pkl", "rb") as fichier:
        return pickle.load(fichier)


def save_default_personne_dead(personne):
    repartition = DeadRepartition(personne=personne)
    repartition.save_default_personne_dead()


def laod_default_personne_dead():
    import pickle
    with open("default_personne_dead.pkl", "rb") as fichier:
        return pickle.load(fichier)


class DeadRepartition:
    def __init__(self, personne: Personne):
        self.__personne = personne

        # On calcul à l'initialisation.
        self.__calcul_indemnite()
        pass

    def __calcul_indemnite(self):
        # On calcule d'abord le préjudice économique des ayants droits
        PrejudiceEconomiqueEnfants(self.__personne)
        PrejudiceEconomiqueConjoints(self.__personne)
        try:
            PrejudiceEconomiqueAscendants(self.__personne)
        except Exception as e:
            print(e)

        # PrejudiceMoral, ControlePlafondPrejudiceMoral
        PrejudiceMoral(self.__personne)

        # Puis, on le compare au plafond fixé par le code CIMA.
        ControlePlafondPrejudiceEconomique(self.__personne)
        ControlePlafondPrejudiceMoral(self.__personne)

    # Cette propriété nous permet de sauvegarder la personne après les différents calculs.
    def save_default_personne_dead(self):
        import pickle
        print("Sauvegade d'une victime dead...")
        with open("default_personne_dead.pkl", "wb") as fichier:
            pickle.dump(self.__personne, fichier)


class DataController:
    def __init__(self):
        self.__func_dict = {} # Il contiendra les noms des fonctions et leurs clés pour les appels futurs.
        self.__data_dict = {"frais_cumul": 0.0,
                            "indemnite_it": 0.0,
                            "indemnite_ip": 0.0,
                            "assistance_tp": 0.0,
                            "pretium_doloris": 0.0,
                            "prejudice_esthetique": 0.0,
                            "perte_gain_pro": 0.0,
                            "prejudice_scolaire": 0.0,
                            "prejudice_moral_conjoint": 0.0,
                            "prejudice_physiologique" : 0.0,
                            "pe_enfants": 0.0,
                            "pe_conjoints": 0.0,
                            "pe_ascendants": 0.0,
                            "pm_enfants": 0.0,
                            "pm_conjoints": 0.0,
                            "pm_ascendants": 0.0,
                            "pm_collateraux": 0.0,
                            } # Il contiendra les données au cours de l'exécution du programme.
        self.load_profil_alive: bool = True
        pass

    def call_fonction(self, key: str):
        callback_function = self.__func_dict.get(key)

        if not callable(callback_function):
            print("Something wrong happened !")
            return

        callback_function() # Appel de la fonction.

    def add_callable_function(self, key: str, func ):
        self.__func_dict[key] = func

    def save_data(self, key: str, value: object):
        self.__data_dict[key] = value
        pass

    def load_data(self, key: str):
        return self.__data_dict.get(key)

    def set_all_value_null(self):
        for key in ["frais_cumul", "indemnite_it", "indemnite_ip", "assistance_tp",
                    "perte_gain_pro", "prejudice_scolaire", "prejudice_moral_conjoint"]:
            self.save_data(key=key, value=0.0)
        pass

#=======================================================================================================================

def format_nombre_fr(nombre, decimales=2):
    """
    Formate un nombre selon les conventions françaises
    :param nombre: Nombre à formater (int, float ou str numérique)
    :param decimales: Nombre de décimales à afficher
    :return: Chaîne formatée
    """
    # Gestion des types et conversion
    if isinstance(nombre, str):
        try:
            nombre = float(nombre) if '.' in nombre else int(nombre)
        except ValueError:
            return nombre  # Retourne la chaîne originale si conversion impossible

    # Séparation partie entière/décimale
    if isinstance(nombre, int):
        partie_entiere = str(abs(nombre))
        partie_decimale = ''
    else:
        partie_entiere, partie_decimale = f"{abs(nombre):.{decimales}f}".split('.')

    # Ajout des espaces comme séparateurs de milliers
    partie_entiere_formatee = []
    longueur = len(partie_entiere)

    for i, chiffre in enumerate(partie_entiere, 1):
        partie_entiere_formatee.append(chiffre)
        if (longueur - i) % 3 == 0 and i != longueur:
            partie_entiere_formatee.append(' ')

    # Assemblage final
    signe = '-' if nombre < 0 else ''
    nombre_formate = signe + ''.join(partie_entiere_formatee)

    if partie_decimale:
        nombre_formate += ',' + partie_decimale

    return nombre_formate


data_contoller = DataController()
save_default_personne_alive(default_personne)
save_default_personne_dead(default_personne)

if __name__ == '__main__':
    print("Chargement du fichier api.py réussi !")