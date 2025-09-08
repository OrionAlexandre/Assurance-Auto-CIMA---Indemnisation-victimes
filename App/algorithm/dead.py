"""
Ce fichier contiendra l'algorithme relatif au calcul de l'indemnité des victimes ayant
succombées à un sinistre automibile.
"""
import logging

from .profils import Personne, Enfant, Conjoint, Ascendant
from .tables import smig_pays_cima_2025, Repartition, TableTemporaire25, TableViagere100, AGE_MAJORITE


# Configuration
logging.basicConfig(
    filename="mon_app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)


class CleDeRepartition(Repartition):
    def __init__(self, personne: Personne):
        self.personne: Personne = personne
        super().__init__()

    def repartition(self):
        if len(self.personne.conjoints) >= 1 and len(self.personne.enfants) <= 4:
            # Nous comptons au moins un conjoint et au plus quatre enfants.
            return self.au_plus_quatre_enfants()
        elif len(self.personne.conjoints) >= 1 and len(self.personne.enfants) > 4:
            # Nous comptons au moins un conjoint et au moins quatre enfants.
            return self.plus_de_quatre_enfants()
        elif len(self.personne.conjoints) == 0 and len(self.personne.enfants) == 0:
            # Nous ne comptons aucun conjoint ni aucun enfant.
            return self.sans_conjoint_sans_enfants()
        elif len(self.personne.conjoints) >= 1 and len(self.personne.enfants) == 0:
            # Nous comptons au moins un conjoint et aucun enfant.
            return self.avec_conjoints_sans_enfants()
        else:
            # Nous ne comptons aucun conjoint, mais au moins un enfant.
            return self.avec_enfants_sans_conjoints()

    def au_plus_quatre_enfants(self): # Ou jusqu'à quatre enfants.
        self.ascendants: int = 5
        self.conjoints: int = 40
        self.enfants: int = 30
        self.enfants_orphelins_double: int = 50
        pass

    def plus_de_quatre_enfants(self):
        self.ascendants: int = 5
        self.conjoints: int = 35
        self.enfants: int = 40
        self.enfants_orphelins_double: int = 50
        pass

    def sans_conjoint_sans_enfants(self):
        self.ascendants: int = 25
        self.conjoints: int = 0
        self.enfants: int = 0
        self.enfants_orphelins_double: int = 0
        pass

    def avec_conjoints_sans_enfants(self):
        self.ascendants: int = 15
        self.conjoints: int = 40
        self.enfants: int = 0
        self.enfants_orphelins_double: int = 0
        pass

    def avec_enfants_sans_conjoints(self):
        self.ascendants: int = 15
        self.conjoints: int = 0
        self.enfants: int = 50
        self.enfants_orphelins_double: int = 60
        pass
    pass


class PrejudiceEconomiqueEnfants:
    def __init__(self, personne: Personne):
        self.personne: Personne = personne
        self.enfants = self.personne.enfants

        self.smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        self.smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)
        self.smig = max(self.smig_sinistre, self.smig_residence)

        # Instanciation de la clé de répartition.
        self.cle_de_repartion = CleDeRepartition(personne=self.personne)

        self.valeur_pour_chaque_enfant() # Appel de la méthode de répartition du préjudice économique des enfants.
        pass

    @property
    def __presence_orphelin_double(self):
        for enfant in self.enfants:
            if enfant.orphelin_double:
                return True # On arrête la boucle puisque l'on a trouvé un orphelin double.
        return False #

    # Détermination du taux enfant à utiliser (orphelin simple ou orphelin double)
    def taux_enfants(self):
        # Si l'on note la présence d'orphelin double, l'on prend le considère le taux propre aux orphelins doubles.
        if self.__presence_orphelin_double:
            return self.cle_de_repartion.enfants_orphelins_double / 100
        # Sinon l'on se sert du taux simple pour les enfants.
        return self.cle_de_repartion.enfants / 100

    @property
    def revenu_net_annuel(self):
        return 12 * self.personne.salaire if self.personne.salaire != 0 else 12 * self.smig

    def bareme_capitalisation(self, enfant: Enfant):
        match enfant.handicap_majeur:
            case False:
                # L'enfant n'a aucun handicap majeur, il peut dont entrer dans la vie active et se prendre en main à l'âge adulte.
                if enfant.poursuit_etudes and enfant.age < 25:
                    return TableTemporaire25(personne=enfant).bareme()
                elif not enfant.poursuit_etudes and enfant.age < AGE_MAJORITE: # Pour le cas des enfants mineurs.
                    return TableTemporaire25(personne=enfant).bareme()
                elif not enfant.poursuit_etudes and enfant.age >= AGE_MAJORITE:
                    return 0.0
                else:
                    return 0.0
            case True:
                # Si l'enfant présente un handicap majeur, sa situation s'apparente à une charge à vie. La table considérée est la table viagère.
                return TableViagere100(personne=enfant).bareme()
        return 0.0 # Dans un non pris en compte dans l'algorithme.

    @property
    def valeur(self):
        # La valeur du préjudice économique à partager entre les enfants de la victime décédée.
        # Le nombre d'enfants.
        nombre_enfants = len(self.personne.enfants)
        return self.taux_enfants() * self.revenu_net_annuel / nombre_enfants

    def valeur_pour_chaque_enfant(self):
        """
        Affecte à chaque la valeur de son préjudice économqie
        Cette méthode affecte ladite valeur à l'attribut correspondant dans la classe enfant.
        Une autre classe servira à s'assurer que les plafonds fixés par le code CIMA ne seront pas dépassés.
        :return:
        """
        # Attrivbution de la valeur du préjudice à chaque enfant.
        for enfant in self.personne.enfants:
            enfant.prejudice_economique = self.valeur * self.bareme_capitalisation(enfant=enfant)
        pass
    pass


class PrejudiceEconomiqueConjoints:
    def __init__(self, personne: Personne):
        self.personne: Personne = personne
        self.conjoints = self.personne.conjoints

        self.smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        self.smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)
        self.smig = max(self.smig_sinistre, self.smig_residence)

        # Instanciation de la clé de répartition.
        self.cle_de_repartion = CleDeRepartition(personne=self.personne)

        self.valeur_pour_chaque_conjoint()
        pass

    def taux_conjoints(self):
        return self.cle_de_repartion.conjoints / 100

    @property
    def revenu_net_annuel(self):
        return 12 * self.personne.salaire if self.personne.salaire != 0 else 12 * self.smig

    def bareme_capitalisation(self, conjoint):
        return TableViagere100(personne=conjoint).bareme()

    def valeur(self):
        nombre_conjoints = len(self.personne.conjoints)
        return self.taux_conjoints() * self.revenu_net_annuel / nombre_conjoints

    def valeur_pour_chaque_conjoint(self):
        for conjoint in self.personne.conjoints:
            conjoint.prejudice_economique = self.valeur() * self.bareme_capitalisation(conjoint=conjoint)

    pass


class PrejudiceEconomiqueAscendants:
    def __init__(self, personne: Personne):
        self.personne: Personne = personne
        self.ascendants = self.personne.ascendants

        self.smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        self.smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)
        self.smig = max(self.smig_sinistre, self.smig_residence)

        # Instanciation de la clé de répartition.
        self.cle_de_repartion = CleDeRepartition(personne=self.personne)

        self.valeur_pour_chaque_ascendant()
        pass

    def taux_ascendants(self):
        return self.cle_de_repartion.ascendants / 100

    @property
    def revenu_net_annuel(self):
        return 12 * self.personne.salaire if self.personne.salaire != 0 else 12 * self.smig

    def bareme_capitalisation(self, ascendant):
        return TableViagere100(personne=ascendant).bareme()

    def valeur(self):
        nombre_ascendants = len(self.personne.ascendants)
        return self.taux_ascendants() * self.revenu_net_annuel / nombre_ascendants

    def valeur_pour_chaque_ascendant(self):
        for ascendant in self.personne.ascendants:
            ascendant.prejudice_economique = self.valeur() * self.bareme_capitalisation(ascendant=ascendant)

    pass


class ControlePlafondPrejudiceEconomique:
    def __init__(self, personne: Personne):
        """
        Cette classe est destinée à s'assurer que le montant du préjudice économique ne dépasse pas le plafond fixé par le
        code CIMA.
        Dans le cas où le total du préjudice économique serait inférieur au plafond aucune redistriution n'est faite.
        Mais dans le cas contraire, ledit préjudice est redistribué dans la limite du plafond fixé par le code tout en considérant
        la part de chaque ayant audit préjudice dans la première distribution.
        :param personne:
        """
        self.personne = personne

        # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
        smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)

        # Définition du smig à retenir pour le calcul du plafond et des indemnités.
        self.smig = max(smig_residence,
                        smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

        self.plafond = 85 * 12 * self.smig  # Quatre-vingt-cinq fois le SMIG annuel.

        # On appelle la méthode des nouvelles répartitions afin de mettre à jour les indemnités alloués.
        self.__repartition_nouvelle()
        pass

    @property
    def total_prejudice_economique(self) -> float:
        # On détermine le montant du préjudice économique.
        liste_pe_enfants = [enfant.prejudice_economique for enfant in self.personne.enfants]
        liste_pe_conjoints = [conjoint.prejudice_economique for conjoint in self.personne.conjoints]
        liste_pe_ascendants = [ascendant.prejudice_economique for ascendant in self.personne.ascendants]
        return sum([*liste_pe_enfants, *liste_pe_conjoints, *liste_pe_ascendants])

    @property
    def plafond_depasse(self) -> bool:
        return True if self.total_prejudice_economique > self.plafond else False

    def __repartition_nouvelle(self):
        # On s'assure que le plafond n'est pas dépassé, sinon on reste dans la fonction.
        # Si le plafond n'est pas dépassé, on ne fait rien.
        if not self.plafond_depasse:
            return

        # Renseignement du fichier log
        self.__info_fichier_log()

        # Détermination des proportions au niveau des enfants.
        self.__determination_des_proportions(list_personnes=self.personne.enfants)

        # Détermination des proportions au niveau des conjoints.
        self.__determination_des_proportions(list_personnes=self.personne.conjoints)

        # Détermination des proportions au niveau des ascendants.
        self.__determination_des_proportions(list_personnes=self.personne.ascendants)

        # Réassignation des nouvelles parts aux enfants.
        self.__reatribution_des_indemnites(list_personnes=self.personne.enfants)

        # Réassignation des nouvelles parts aux conjoints.
        self.__reatribution_des_indemnites(list_personnes=self.personne.conjoints)

        # Réassignation des nouvelles parts aux ascendants.
        self.__reatribution_des_indemnites(list_personnes=self.personne.ascendants)

        # Renseignement du fichier log
        self.__info_fichier_log(entree=False) # Nous sommes à la sortie.
        pass

    def __determination_des_proportions(self, list_personnes: list[Enfant] | list[Conjoint] | list[Ascendant]):
        # On ramène le préjudice économqie de chaque personne au montant total afin de trouver la proportion dans laquelle
        # il est indemnisé par rapport aux autres.
        for personne in list_personnes:
            personne.proportion = personne.prejudice_economique / self.total_prejudice_economique
        pass

    def __reatribution_des_indemnites(self, list_personnes: list[Enfant] | list[Conjoint] | list[Ascendant]):
        # On multiplie la proportion de chaque ayant droit par le plafond afin de rester dans les mêmes cotités.
        for personne in list_personnes:
            personne.prejudice_economique = personne.proportion * self.plafond
        pass

    def __info_fichier_log(self, entree: bool = True):
        message = "Entrée dans la méthode de répartition\n" if entree else "Sortie de la méthode de répartition\n"
        message += "-" * 65 + "\n"
        message += "-" * 65 + "\n"
        message += " " * 30 + "Préjudice économique \n"
        message += "-" * 65 + "\n"
        message += f"Plafond : {self.plafond}\n"
        message += "Part de chaque enfant :\n"

        for enfant in self.personne.enfants:
            message += f"  - {enfant.nom} {enfant.prenom} : {round(enfant.prejudice_economique, 2)} F CFA\n"
        message += "Proportion de chaque enfant :\n"
        for enfant in self.personne.enfants:
            message += f"  - {enfant.nom} {enfant.prenom} : {round(enfant.proportion * 100, 2)}%\n"

        message += "Part de chaque conjoint :\n"
        for conjoint in self.personne.conjoints:
            message += f"  - {conjoint.nom} {conjoint.prenom} : {round(conjoint.prejudice_economique, 2)} F CFA\n"
        message += "Proportion de chaque conjoint :\n"
        for conjoint in self.personne.conjoints:
            message += f"  - {conjoint.nom} {conjoint.prenom} : {round(conjoint.proportion * 100, 2)}%\n"

        message += "Part de chaque ascendant :\n"
        for ascendant in self.personne.ascendants:
            message += f"  - {ascendant.nom} {ascendant.prenom} : {round(ascendant.prejudice_economique, 2)} F CFA\n"
        message += "Proportion de chaque ascendant :\n"
        for ascendant in self.personne.ascendants:
            message += f"  - {ascendant.nom} {ascendant.prenom} : {round(ascendant.proportion * 100, 2)}%\n"

        logging.info(message)
        pass

    pass


class PrejudiceMoral:
    def __init__(self, personne: Personne):
        """
        Article 266 code CIMA.
        :param personne:
        """
        self.personne = personne

        self.taux_conjoints = 150 / 100 # Le / 100 permet de considérer le taux en pourcentage.
        self.taux_enfants_mineurs = 100 / 100
        self.taux_enfants_majeurs = 75 / 100
        self.taux_ascendants = 75 / 100
        self.taux_collateraux = 50 / 100 # Les frères et sœurs.

        # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
        smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)

        # Définition du smig à retenir pour le calcul du plafond et des indemnités.
        self.smig = max(smig_residence,
                        smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

        # Appel des méthodes de calcul du préjudice moral.
        self.__prejudice_moral_par_ascendant()
        self.__prejudice_moral_par_collateral()
        self.__prejudice_moral_par_conjoints()
        self.__prejudice_moral_par_enfant()
        pass

    @property
    def smig_annuel(self):
        return 12 * self.smig

    def __taux_enfant(self, enfant: Enfant):
        return self.taux_enfants_majeurs if enfant.age >= AGE_MAJORITE else self.taux_enfants_mineurs

    def __prejudice_moral_par_enfant(self):
        for enfant in self.personne.enfants:
            enfant.prejudice_moral = self.__taux_enfant(enfant) * self.smig_annuel
        pass

    def __prejudice_moral_par_conjoints(self):
        for conjoint in self.personne.conjoints:
            conjoint.prejudice_moral = self.taux_conjoints * self.smig_annuel
        pass

    def __prejudice_moral_par_ascendant(self):
        for ascendant in self.personne.ascendants:
            ascendant.prejudice_moral = self.taux_ascendants * self.smig_annuel
        pass

    def __prejudice_moral_par_collateral(self):
        for collateral in self.personne.collateraux:
            collateral.prejudice_moral = self.taux_collateraux * self.smig_annuel
        pass

    pass


class ControlePlafondPrejudiceMoral:
    def __init__(self, personne: Personne):
        self.personne = personne

        # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
        smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)

        # Définition du smig à retenir pour le calcul du plafond et des indemnités.
        self.smig = max(smig_residence,
                        smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

        # Nouvelles répartitions après comparaison au SMIG.
        self.__repartition_nouvelle()
        self.__repartition_nouvelle_conjoints()
        pass

    @property
    def plafond_global(self):
        # L'indemnité globale due au titre du préjudice moral des ayants droit ne saurait être supérieure à 20 fois le smig annuel.
        return 20 * 12 * self.smig

    @property
    def plafond_conjoints(self):
        # L'indemnité globale due au titre du préjudice moral des conjoints de la victime, s'il y en a plus d'un,
        # ne saurait être supérieure à six fois le smig annuel.
        return 6 * 12 * self.smig

    @property
    def total_prejudice_moral(self):
        pm_enfants = [enfant.prejudice_moral for enfant in self.personne.enfants]
        pm_conjoints = [conjoint.prejudice_moral for conjoint in self.personne.conjoints]
        pm_collateraux = [collateral.prejudice_moral for collateral in self.personne.collateraux]
        return sum([*pm_enfants, *pm_conjoints, *pm_collateraux])

    @property
    def plafond_global_depasse(self) -> bool:
        return True if self.total_prejudice_moral > self.plafond_global else False

    @property
    def plafond_conjoints_depasse(self) -> bool:
        return True if sum([conjoint.prejudice_moral for conjoint in self.personne.conjoints]) > self.plafond_conjoints else False

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __repartition_nouvelle(self):
        # On s'assure que le plafond global n'est pas dépassé, sinon on reste dans la fonction.
        # Si ce plafond n'est pas dépassé, on ne fait rien.
        if not self.plafond_global_depasse:
            return

        # Renseignement du fichier log
        self.__info_fichier_log()

        # Détermination des proportions au niveau des enfants.
        self.__determination_des_proportions(list_personnes=self.personne.enfants)

        # Détermination des proportions au niveau des conjoints.
        self.__determination_des_proportions(list_personnes=self.personne.conjoints)

        # Réassignation des nouvelles parts aux enfants.
        self.__reatribution_des_indemnites(list_personnes=self.personne.enfants)

        # Réassignation des nouvelles parts aux conjoints.
        self.__reatribution_des_indemnites(list_personnes=self.personne.conjoints)

        # Renseignement du fichier log
        self.__info_fichier_log(entree=False)  # Nous sommes à la sortie.
        pass

    def __repartition_nouvelle_conjoints(self):
        if not self.plafond_conjoints_depasse:
            return

        # Renseignement du fichier log
        self.__info_fichier_log()

        self.__determination_proportions_conjoints(self.personne.conjoints)
        self.__reatribution_indemnites_conjoints(self.personne.conjoints)

        # Renseignement du fichier log
        self.__info_fichier_log(entree=False)  # Nous sommes à la sortie.
        pass
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __determination_des_proportions(self, list_personnes: list[Enfant] | list[Conjoint]):
        # On ramène le préjudice moral de chaque personne au montant total afin de trouver la proportion dans laquelle
        # il est indemnisé par rapport aux autres.
        for personne in list_personnes:
            personne.proportion = personne.prejudice_moral / self.total_prejudice_moral
        pass

    def __reatribution_des_indemnites(self, list_personnes: list[Enfant] | list[Conjoint]):
        # On multiplie la proportion de chaque ayant droit par le plafond afin de rester dans les mêmes cotités.
        for personne in list_personnes:
            personne.prejudice_moral = personne.proportion * self.plafond_global
        pass

    # Cas des multiples conjoints.
    #-----------------------------
    def __determination_proportions_conjoints(self, list_personnes: list[Conjoint]):
        # On ramène le préjudice moral de chaque personne au montant total afin de trouver la proportion dans laquelle
        # il est indemnisé par rapport aux autres.
        for personne in list_personnes:
            personne.proportion = personne.prejudice_moral / sum([conjoint.prejudice_moral for conjoint in self.personne.conjoints])
        pass

    def __reatribution_indemnites_conjoints(self, list_personnes: list[Conjoint]):
        # On multiplie la proportion de chaque ayant droit par le plafond afin de rester dans les mêmes cotités.
        for personne in list_personnes:
            personne.prejudice_moral = personne.proportion * self.plafond_conjoints
        pass

    # Méthode de renseignement des fichiers logs.
    def __info_fichier_log(self, entree: bool = True):
        message = "Entrée dans la méthode de répartition\n" if entree else "Sortie de la méthode de répartition\n"
        message += "-" * 65 + "\n"
        message += " " * 30 + "Préjudice moral \n"
        message += "-" * 65 + "\n"
        message += f"Plafond : {self.plafond_global}\n"
        message += "Part de chaque enfant :\n"
        for enfant in self.personne.enfants:
            message += f"  - {enfant.nom} {enfant.prenom} : {round(enfant.prejudice_moral, 2)} F CFA\n"
        message += "Proportion de chaque enfant :\n"
        for enfant in self.personne.enfants:
            message += f"  - {enfant.nom} {enfant.prenom} : {round(enfant.proportion * 100, 2)}%\n"
        message += "Part de chaque conjoint :\n"
        for conjoint in self.personne.conjoints:
            message += f"  - {conjoint.nom} {conjoint.prenom} : {round(conjoint.prejudice_moral, 2)} F CFA\n"
        message += "Proportion de chaque conjoint :\n"
        for conjoint in self.personne.conjoints:
            message += f"  - {conjoint.nom} {conjoint.prenom} : {round(conjoint.proportion * 100, 2)}%\n"

        logging.info(message)
        pass

    pass


class Frais:
    def __init__(self, personne: Personne, valeur: float = 0.0):
        self.personne = personne
        self.__valeur = valeur

        # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
        smig_residence = smig_pays_cima_2025.get(self.personne.pays_residence)
        smig_sinistre = smig_pays_cima_2025.get(self.personne.pays_sinistre)

        # Définition du smig à retenir pour le calcul du plafond et des indemnités.
        self.smig = max(smig_residence,
                        smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

    @property
    def plafond(self):
        # Deux smig annuel.
        return 2 * 12 * self.smig

    @property
    def valeur(self):
        return self.__valeur if self.__valeur <= self.plafond else self.plafond

    @valeur.setter
    def valeur(self, valeur):
        self.__valeur = valeur
    pass
