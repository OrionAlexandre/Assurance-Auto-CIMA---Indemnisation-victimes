"""
Ce fichier contiendra l'algorithme relatif au calcul de l'indemnité des victimes ayant
survécues à un sinistre automibile.
"""

from algorithm.profils import Personne
from algorithm.tables import (smig_pays_cima_2025, ValeurPointIP, TableTemporaire21, TableTemporaire25, TableTemporaire55,
                    TableTemporaire60, TableTemporaire65, TableViagere100)


class FraisDeTraitement:
    def __init__(self):
        """
        Article 258 Code CIMA.
        """
        self.__valeur: float = 0.0

    @property
    def valeur(self):
        return self.__valeur

    @valeur.setter
    def valeur(self, valeur: float = 0.0):
        self.__valeur = valeur if valeur >= 0 else 0.0

    pass


class IncapaciteTemporaire:
    """
    Article 259 Code CIMA.
    """
    def __init__(self, personne: Personne, duree: int, taux_it: float = 100.0):
        self.personne = personne # Il s'agit de la victime.
        self.age = self.personne.age # l'age de la personne.
        self.taux_it = taux_it # Le taux d'IP.
        self.duree = duree # Le nombre de jours que durera l'incapacité temporaire.

        # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
        smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)

        # Définition du smig à retenir pour le calcul du plafond et des indemnités.
        self.smig = max(smig_residence, smig_sinistre) # Le plus grand des deux smig selon les dispositions du Code CIMA.

    @property
    def plafond(self):
        # Selon que la victime justifie d'une mensualité ou non.
        if self.personne.salaire != 0 or self.personne.profession != "":
            return self.smig * 12 * 6 # Six fois le smig annuel.
        # Sinon (Le code étant muet)
        return 0.0

    @property
    def __salaire_moyen_journalier(self):
        return self.personne.salaire / 30

    # Le cas d'une victime salariée ou pouvant justifier d'une mensualité.
    def incapacite_temporaire_partielle(self) -> float:
        # La victime reprend son travail, mais du fait de l'incapacité n'est plus aussi performante, de ce fait,
        # elle subit une réduction salaire.
        # La victime est indemnisée à la hauteur de la perte de revenu mensuel.
        valeur = self.__salaire_moyen_journalier * self.taux_it / 100 * self.duree

        # L'indemnité est plafond à la valeur ici définit comme plafond. min() retourne la valeur la plus petite,
        # don le plafond si la valeur lui est supérieure.
        return min(valeur, self.plafond)

    def incapacite_temporaire_totale(self) -> float:
        # La victime sur un certain nombre de jours ne retourne à son travail.
        # La victime est rémunérée à la hauteur de la perte de revenu rapporté au taux d'incapacité.
        valeur = self.__salaire_moyen_journalier * self.duree
        return min(valeur, self.plafond)
    pass


class IncapacitePermanente:
    """
    Article 260 du Code CIMA.
    """
    def __init__(self, personne: Personne, salaire_apres_accident:float, taux_ip: float = 100.0):
        self.personne = personne
        self.salaire_apres_accident = salaire_apres_accident
        self.taux_ip = taux_ip

        # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
        smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)

        # Définition du smig à retenir pour le calcul du plafond et des indemnités.
        self.smig = max(smig_residence, smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

    @property
    def bareme(self):
        match self.personne.age_limite:
            case 21:
                return TableTemporaire21(personne=self.personne).bareme()
            case 25:
                return TableTemporaire25(personne=self.personne).bareme()
            case 55:
                return TableTemporaire55(personne=self.personne).bareme()
            case 60:
                return TableTemporaire60(personne=self.personne).bareme()
            case 65:
                return TableTemporaire65(personne=self.personne).bareme()
            case 100:
                return TableViagere100(personne=self.personne).bareme()
        return 0.0

    @property
    def valeur_point_ip(self):
        # Retourne le point d'IP en fonction de l'age de la personne et de son taux d'IP.
        if self.personne.age <= 100:
            return ValeurPointIP(person=self.personne, taux_ip=self.taux_ip).valeur
        return 0.0

    def prejudice_physiologique(self):
        return (self.smig * 12 * self.valeur_point_ip / 100) * self.taux_ip

    def prejudice_economique(self):
        # À condition que le taux d'incapacité soit supérieur à 50%.
        if self.taux_ip < 50:
            return 0.0
        valeur = (self.personne.salaire - self.salaire_apres_accident) * 12 * self.bareme
        plafond = 10 * 12 * self.smig
        return min(valeur, plafond) # Article 260 - b

    def prejudice_moral(self):
        # À condition que le taux d'incapacité soit supérieur à 80%.
        if self.taux_ip < 80:
            return 0.0
        return 2 * 12 * self.smig # Article 260 - c

    def valeur(self):
        return sum([self.prejudice_physiologique(),
                    self.prejudice_economique(),
                    self.prejudice_moral()])

    pass


class AssistanceTiercePersonne(IncapacitePermanente):
    """
    Article 262 Code CIMA :
        L'assistance doit faire l'objet d'une prescription médicale expresse confirmée par expertise.
        L'indemnité allouée à ce titre est plafonnée à 50 % de l'indemnité fixée pour l'incapacité
        permanente.
    Hérite de la classe IncapacitePermanente, l'assistance ne se calcule qu'à la suite de l'incapacité permanente.
    """

    def __init__(self, personne: Personne, salaire_apres_accident:float, taux_ip: float = 100.0):
        super().__init__(personne=personne, salaire_apres_accident=salaire_apres_accident, taux_ip=taux_ip)

    def valeur(self):
        return sum([
            self.prejudice_physiologique(),
            self.prejudice_economique(),
            self.prejudice_moral(),
        ]) * 0.5 if self.taux_ip >= 80.0 else 0.0
    pass


class PrejudiceEsthetique:
    def __init__(self, personne: Personne, niveau: int):
        """

        :param personne: La victime de l'accident, instance de la class Personne.
        :param niveau: NiveauPrejudice.tres_leger
        """
        self.personne = personne
        self.niveau = niveau

        self.smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        self.smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)
        self.smig = max(self.smig_sinistre, self.smig_residence)

    def valeur(self):
        return 12 * self.smig * self.niveau / 100
    pass


class PretiumDoloris:
    """

    :param personne: La victime de l'accident, instance de la class Personne.
    :param niveau: NiveauPrejudice.tres_leger
    """
    def __init__(self, personne: Personne, niveau: int):
        self.personne = personne
        self.niveau = niveau

        self.smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        self.smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)
        self.smig = max(self.smig_sinistre, self.smig_residence)

    def valeur(self):
        return 12 * self.smig * self.niveau / 100
    pass


class PrejudicePerteDeGainsProfessinnelsFuturs:
    """
    Article 263 Code CIMA.\n
    Le préjudice de pertes de gains professionnels futurs s’entend de la perte de carrière subie par
    une personne déjà engagée dans la vie active.
    L'indemnité est limitée à six mois de revenus calculés et plafonnés à trente-six fois le SMIG
    annuel du pays de l’accident, ou, s’il y est plus élevé, du pays de l’espace CIMA où la victime a sa
    résidence habituelle.
    """
    def __init__(self, personne: Personne):
        self.personne: Personne = personne

        # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
        smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)

        # Définition du smig à retenir pour le calcul du plafond et des indemnités.
        self.smig = max(smig_residence,
                        smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

    @property
    def plafond(self):
        return 36 * 12 * self.smig

    def valeur(self):
        valeur = 6 * self.personne.salaire
        return min(valeur, self.plafond)
    pass


class PrejudiceScolaire:
    """
    Article 263-1 Code CIMA.\n
    Le préjudice scolaire s’entend de la perte de chance certaine d'une carrière à laquelle peut
    raisonnablement espérer un élève ou un étudiant de l'enseignement primaire, supérieur ou leur
    équivalent ;
    L'indemnité à allouer est limitée à douze mois de bourse officielle de la catégorie correspondante.

    De ce cas, le salaire de la personne est entendu comme étant la bourse officielle de l'élève ou de l'étudiant.
    """
    def __init__(self, personne: Personne):
        self.personne: Personne = personne
        self.bourse_officielle: float = self.personne.salaire

    def valeur(self):
        return 12 * self.bourse_officielle
    pass


class PrejudiceMoralConjoint:
    """
     Le préjudice subi par les personnes physiques qui établissent être en communauté de vie avec la
     victime directe de l'accident peut ouvrir droit à réparation dans les limites ci-après :\n
     - en cas de blessures graves réduisant totalement la capacité de la victime directe, seul(s) le(s) conjoint(s) sont admis à obtenir réparation du préjudice moral subi, et ce, dans la limite de \
     deux SMIG annuels, pour l'ensemble des bénéficiaires ;
    """
    def __init__(self, personne: Personne, taux_ip: float):
        self.personne: Personne = personne
        self.taux_ip: float = taux_ip

        # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
        smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)

        # Définition du smig à retenir pour le calcul du plafond et des indemnités.
        self.smig = max(smig_residence,
                        smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

    def valeur(self):
        if not self.personne.conjoints or self.taux_ip != 100:
            return 0 # La victime n'a pas de conjoint n'est pas à 100% invalide.
        valeur = 2 * 12 * self.smig # Les deux conditions précendentes sont vérifiées.
        return valeur
    pass
