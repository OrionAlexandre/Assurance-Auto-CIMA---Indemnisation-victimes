from .alive import IncapaciteTemporaire, IncapacitePermanente
from .dead import PrejudiceEconomiqueConjoints, ControlePlafondPrejudiceEconomique, PrejudiceEconomiqueEnfants
from .profils import Enfant, Conjoint, Personne

from .tables import SituationMatrimoniale

# Les fonctions d'affichage des résultats issus des tests.
def afficher_prejudice_economique_enfants(personne: Personne, pe_enfants: PrejudiceEconomiqueEnfants):
    print("*" * 63)
    print("*" * 10 + "Calcul du préjudice économique des enfants" + "*" * 10)
    print("*" * 63)
    print(f"Nom : {personne.enfants[0].nom} | Prénom : {personne.enfants[0].prenom}")
    print(f"Valeur du préjudice économique : {personne.enfants[0].prejudice_economique}")
    print("_" * 60)
    print(f"Nom : {personne.enfants[1].nom} | Prénom : {personne.enfants[1].prenom}")
    print(f"Valeur du préjudice économique : {personne.enfants[1].prejudice_economique}")
    print("_" * 60)
    print(f"Taux de répartition pour les enfants : {pe_enfants.taux_enfants()}")

def afficher_prejudice_economique_conjoints(personne: Personne, pe_conjoints: PrejudiceEconomiqueConjoints):
    print("*" * 63)
    print("*" * 10 + "Calcul du préjudice économique des conjoints" + "*" * 10)
    print("*" * 63)
    for i in range(len(personne.conjoints)):
        print(f"Nom : {personne.conjoints[i].nom} | Prénom : {personne.conjoints[i].prenom}")
        print(f"Valeur du préjudice économique : {personne.conjoints[i].prejudice_economique}")
        print(
            f"Le barème de capitalisation pour {personne.conjoints[i].nom} : {pe_conjoints.bareme_capitalisation(personne.conjoints[i])}")
        print("_" * 60)
    print(f"Taux de répartition pour les conjoints : {pe_conjoints.taux_conjoints()}")


# Test de l'incapacité temporaire.
def test_it_jean():
    # nous instancions une personne.
    Jean = Personne(
        nom="VIANNEY",
        prenom="Jean-marie",
        age=23,
        sexe="M",
        profession="Paroissien",
        salaire=150_000,
        age_limite=60,
        situation_matrimoniale=SituationMatrimoniale.CELIBATAIRE,
        conjoints=[],
        enfants=[],
        ascendants=[],
        collateraux=[],
        pays_residence="Congo",
        pays_sinistre="Togo",
    )

    it = IncapaciteTemporaire(personne=Jean, duree=6, taux_it=40)

    print("=" * 30)
    print(Jean.nom, Jean.prenom, Jean.age, "ans", "Sexe:", Jean.sexe)
    print("Taux d'IT: " + str(it.taux_it) + "%")
    print("Salaire avant le sinistre: " + str(Jean.salaire) + " F CFA")
    print(f"Jean a une incapacité temporaire partielle de {it.duree} de jours, son indemnité est de : " + str(
        it.incapacite_temporaire_partielle()) + " F CFA.")
    print("Plafond: ", it.plafond)

# Test de l'incapacité permanente.
def test_ip_jean_1():
    # nous instancions une personne.
    Jean = Personne(
        nom="VIANNEY",
        prenom="Jean-marie",
        age=45,
        sexe="M",
        profession="Paroissien",
        salaire=300_000,
        age_limite=60,
        situation_matrimoniale=SituationMatrimoniale.CELIBATAIRE,
        conjoints=[],
        enfants=[],
        ascendants=[],
        collateraux=[],
        pays_residence="Congo",
        pays_sinistre="Togo",
    )

    ip = IncapacitePermanente(personne=Jean, salaire_apres_accident=285000, taux_ip=65)
    print("=" * 30)
    print(Jean.nom, Jean.prenom, Jean.age, "ans", "Sexe:", Jean.sexe)
    print("Taux d'IP: " + str(ip.taux_ip) + "%")
    print("Salaire avant le sinistre: " + str(Jean.salaire) + " F CFA")
    print("Salaire après le sinistre: " + str(ip.salaire_apres_accident) + " F CFA")
    print("Préjudice physiologique", ip.prejudice_physiologique(), "F CFA")
    print("Préjudice économique", ip.prejudice_economique(), "F CFA")
    print("Préjudice moral", ip.prejudice_moral(), "F CFA")


# Test du préjudice économque des ayants droits.
def test_indemnite_economique_1():
    rosalie = Enfant(
        nom="MAYEGA",
        prenom="Rosalie",
        age=23,
        sexe="F",
        handicap_majeur=False,
    )
    rene = Enfant(
        nom="MAYEGA",
        prenom="René",
        age=15,
        sexe="M",
        handicap_majeur=False,
    )
    marie = Conjoint(
        nom="MAYIGA",
        prenom="Marie",
        age=35,
    )
    germaine = Conjoint(
        nom="MAYIGA",
        prenom="Germaine",
        age=40,
    )
    personne = Personne(
        nom="MAYEGA",
        prenom="Jean-marie",
        age=23,
        sexe="M",
        profession="Paroissien",
        salaire=150_000,
        age_limite=60,
        situation_matrimoniale=SituationMatrimoniale.CELIBATAIRE,
        conjoints=[marie, germaine],
        enfants=[rosalie, rene],
        ascendants=[],
        collateraux=[],
        pays_residence="Congo",
        pays_sinistre="Togo",
    )

    # On calcule d'abord le préjudice économique des ayants droits
    pe_enfants = PrejudiceEconomiqueEnfants(personne)
    pe_conjoints = PrejudiceEconomiqueConjoints(personne)

    # Puis, on le compare au plafond fixé par le code CIMA.
    controle_pe = ControlePlafondPrejudiceEconomique(personne)

    afficher_prejudice_economique_enfants(personne=personne, pe_enfants=pe_enfants)
    print()
    afficher_prejudice_economique_conjoints(personne=personne, pe_conjoints=pe_conjoints)


def test_indemnite_economique_2():
    rosalie = Enfant(
        nom="MAYEGA",
        prenom="Rosalie",
        age=23,
        sexe="F",
        handicap_majeur=False,
        poursuit_etudes=False
    )
    rene = Enfant(
        nom="MAYEGA",
        prenom="René",
        age=15,
        sexe="M",
        handicap_majeur=False,
        poursuit_etudes=False
    )
    marie = Conjoint(
        nom="MAYIGA",
        prenom="Marie",
        age=35,
    )
    germaine = Conjoint(
        nom="MAYIGA",
        prenom="Germaine",
        age=40,
    )
    personne = Personne(
        nom="MAYEGA",
        prenom="Jean-marie",
        age=23,
        sexe="M",
        profession="Paroissien",
        salaire=150_000,
        age_limite=60,
        situation_matrimoniale=SituationMatrimoniale.CELIBATAIRE,
        conjoints=[marie, germaine],
        enfants=[rene, rosalie],
        ascendants=[],
        collateraux=[],
        pays_residence="Congo",
        pays_sinistre="Togo",
    )

    pe_enfants = PrejudiceEconomiqueEnfants(personne)
    pe_conjoints = PrejudiceEconomiqueConjoints(personne)
    controle_pe = ControlePlafondPrejudiceEconomique(personne)

    afficher_prejudice_economique_enfants(personne=personne, pe_enfants=pe_enfants)
    print()
    afficher_prejudice_economique_conjoints(personne=personne, pe_conjoints=pe_conjoints)


def test_indemnite_economique_3():
    remi = Enfant(
        nom="MAYEGA",
        prenom="Rémi",
        age=22,
        sexe="M",
        poursuit_etudes=True,
        orphelin_double=True
    )
    personne = Personne(
        nom="MAYEGA",
        prenom="Jean-marie",
        age=23,
        sexe="M",
        profession="Paroissien",
        salaire=150_000,
        age_limite=60,
        situation_matrimoniale=SituationMatrimoniale.CELIBATAIRE,
        conjoints=[],
        enfants=[remi],
        ascendants=[],
        collateraux=[],
        pays_residence="Congo",
        pays_sinistre="Togo",
    )

    pe_enfants = PrejudiceEconomiqueEnfants(personne)
    controle_pe = ControlePlafondPrejudiceEconomique(personne)

    afficher_prejudice_economique_enfants(personne=personne, pe_enfants=pe_enfants)


def test_indemnite_economique_4():
    rosalie = Enfant(
        nom="MAYEGA",
        prenom="Rosalie",
        age=23,
        sexe="F",
        handicap_majeur=False,
    )
    rene = Enfant(
        nom="MAYEGA",
        prenom="René",
        age=15,
        sexe="M",
        handicap_majeur=False,
    )
    remi = Enfant(
        nom="MAYEGA",
        prenom="Rémi",
        age=22,
        sexe="M",
        poursuit_etudes=True,
        orphelin_double=True
    )
    marie = Conjoint(
        nom="MAYIGA",
        prenom="Marie",
        age=35,
    )
    germaine = Conjoint(
        nom="MAYIGA",
        prenom="Germaine",
        age=40,
    )
    personne = Personne(
        nom="MAYEGA",
        prenom="Jean-marie",
        age=23,
        sexe="M",
        profession="Paroissien",
        salaire=150_000,
        age_limite=60,
        situation_matrimoniale=SituationMatrimoniale.CELIBATAIRE,
        conjoints=[marie, germaine],
        enfants=[remi, rene, rosalie],
        ascendants=[],
        collateraux=[],
        pays_residence="Congo",
        pays_sinistre="Togo",
    )

    pe_enfants = PrejudiceEconomiqueEnfants(personne)
    pe_conjoints = PrejudiceEconomiqueConjoints(personne)
    controle_pe = ControlePlafondPrejudiceEconomique(personne)

    afficher_prejudice_economique_enfants(personne=personne, pe_enfants=pe_enfants)
    print()
    afficher_prejudice_economique_conjoints(personne=personne, pe_conjoints=pe_conjoints)


# Test du préjudice moral des ayants droits.
"""
Test à implémenter !
"""


if __name__ == '__main__':
    test_it_jean()