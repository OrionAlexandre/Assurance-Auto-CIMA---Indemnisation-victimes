"""
Ce fichier contiendra le ou les modèles de données qui serviront à alimenter les algoritmes
de calcul.
"""

from .profils import Personne, Enfant, Conjoint, Ascendant
from abc import ABC, abstractmethod


list_pays_cima = [
    "Bénin",
    "Burkina Faso",
    "Cameroun",
    "Centrafrique",
    "Congo",
    "Côte d'Ivoire",
    "Gabon",
    "Guinée Bissau",
    "Guinée Equatoriale",
    "Mali",
    "Niger",
    "Sénégal",
    "Tchad",
    "Togo"
]

AGE_MAJORITE  = 18
AGE_LIMITE = 60

smig_pays_cima_2025 = {
    "Bénin": 52000, # 🕊️
    "Burkina Faso": 45000, # 🕊️
    "Cameroun": 60000, # 🕊️...
    "Centrafrique": 36000,
    "Congo": 70400, # 🕊️
    "Côte d'Ivoire": 75000, # 🕊️
    "Gabon": 150000, # 🕊️
    "Guinée Bissau": 36169, # 550_000 Francs Guinéens

    "Guinée Equatoriale": 128000,
    "Mali": 40000, # 🕊️
    "Niger": 30047, # 🕊️
    "Sénégal": 64223, # 🕊️
    "Tchad": 70400, # 🕊️
    "Togo": 52500
}

doloris_list = [
    "-",
    "Très léger",
    "Léger",
    "Modéré",
    "Moyen",
    "Assez important",
    "Très important",
    "Exceptionnel"
]


class TableViagere100:
    def __init__(self, personne: Personne | Enfant | Conjoint | Ascendant):
        """

        :param personne: La victime
        """
        self.personne = personne

        self.__baremes_masculin: list[float] = \
            [14.576, 14.910, 14.915, 14.903, 14.884, 14.861, 14.835, 14.807, 14.777, 14.744,
            14.709, 14.671, 14.631, 14.588, 14.543, 14.497, 14.450, 14.401, 14.353, 14.304,
            14.253, 14.200, 14.144, 14.086, 14.025, 13.959, 13.891, 13.818, 13.740, 13.658,
            13.571, 13.480, 13.384, 13.284, 13.180, 13.071, 12.958, 12.839, 12.716, 12.588,
            12.455, 12.316, 12.172, 12.023, 11.869, 11.709, 11.544, 11.373, 11.197, 11.016,
            10.829, 10.637, 10.440, 10.237, 10.030, 9.818, 9.602, 9.381, 9.156, 8.928,
            8.696, 8.461, 8.223, 7.983, 7.741, 7.498, 7.254, 7.010, 6.766, 6.523,
            6.282, 6.043, 5.808, 5.577, 5.351, 5.132, 4.921, 4.720, 4.531, 4.356,
            2.707, 3.582, 3.371, 3.167, 2.969, 2.778, 2.593, 2.415, 2.244, 2.081,
            1.924, 1.775, 1.633, 1.498, 1.371, 1.250, 1.136, 1.030, 0.930, 0.836,
            0.748] # Les barêmes

        self.__baremes_feminin: list[float] = \
            [14.806, 15.065, 15.077, 15.072, 15.061, 15.048, 15.033, 15.016, 14.997, 14.976,
             14.953, 14.929, 14.904, 14.876, 14.848, 14.818, 14.787, 14.755, 14.721, 14.686,
             14.650, 14.612, 14.572, 14.529, 14.485, 14.438, 14.388, 14.336, 14.281, 14.223,
             14.163, 14.099, 14.032, 13.961, 13.886, 13.807, 13.724, 13.636, 13.544, 13.448,
             13.346, 13.240, 13.128, 13.011, 12.888, 12.760, 12.625, 12.485, 12.339, 12.186,
             12.026, 11.861, 11.688, 11.509, 11.323, 11.130, 10.931, 10.725, 10.512, 10.293,
             10.067, 9.835, 9.597, 9.352, 9.103, 8.848, 8.588, 8.324, 8.056, 7.784,
             7.509, 7.232, 6.953, 6.672, 6.391, 6.110, 5.830, 5.551, 5.275, 5.001,
             4.731, 4.466, 4.205, 3.950, 3.701, 3.459, 3.224, 2.997, 2.778, 2.567,
             2.365, 2.173, 1.989, 1.815, 1.650, 1.494, 1.348, 1.210, 1.082, 0.963,
             0.851]  # Les barêmes

    def bareme(self) -> float:
        """
        Par coïncidence les indexe de la liste des barêmes vont de 0 à 100, il suffit juste de retourner le barême situé
        à indexer équivalent en âge à l'âge de la Personnene.
        :return : Le barême correspondant à l'âge de la Personnene
        """
        baremes: list[float] = self.__baremes_feminin if self.personne.sexe == "F" else self.__baremes_masculin
        return baremes[self.personne.age] if 0 <= self.personne.age <= 100 else 0.0


class TableTemporaire65:
    def __init__(self, personne: Personne | Enfant | Conjoint | Ascendant):
        """

        :param personne: La victime
        """
        self.personne = personne

        self.__baremes_masculin: list[float] = \
            [14.492, 14.819, 14.818, 14.799, 14.773, 14.743, 14.710, 14.674, 14.634, 14.592,
             14.547, 14.499, 14.447, 14.392, 14.335, 14.276, 14.213, 14.149, 14.084, 14.017,
             13.947, 13.873, 13.796, 13.715, 13.628, 13.537, 13.440, 13.337, 13.228, 13.111,
             12.988, 12.857, 12.720, 12.575, 12.423, 12.263, 12.095, 11.918, 11.731, 11.536,
             11.330, 11.114, 10.886, 10.647, 10.396, 10.132, 9.855, 9.563, 9.255, 8.932,
             8.591, 8.232, 7.854, 7.454, 7.031, 6.583, 6.109, 5.604, 5.068, 4.495,
             3.881, 3.223, 2.513, 1.745, 0.911, 0.000]  # Les barêmes

        self.__baremes_feminin: list[float] = \
            [14.685, 14.935, 14.938, 14.923, 14.903, 14.880, 14.853, 14.824, 14.793, 14.759,
             14.722, 14.683, 14.641, 14.597, 14.550, 14.500, 14.449, 14.394, 14.337, 14.277,
             14.214, 14.148, 14.077, 14.002, 13.923, 13.839, 13.750, 13.655, 13.556, 13.450,
             13.338, 13.220, 13.094, 12.961, 12.820, 12.671, 12.512, 12.344, 12.166, 11.978,
             11.778, 11.567, 11.343, 11.105, 10.854, 10.588, 10.306, 10.008, 9.692, 9.358,
             9.003, 8.628, 8.230, 7.808, 7.360, 6.885, 6.380, 5.844, 5.272, 4.664,
             4.015, 3.321, 2.578, 1.781, 0.924, 0.000]  # Les barêmes

    def bareme(self) -> float:
        """
        Par coïncidence les indexe de la liste des barêmes vont de 0 à 100, il suffit juste de retourner le barême situé
        à indexer équivalent en âge à l'âge de la Personnene.
        :return : Le barême correspondant à l'âge de la Personnene
        """
        baremes: list[float] = self.__baremes_feminin if self.personne.sexe == "F" else self.__baremes_masculin
        return baremes[self.personne.age] if 0 <= self.personne.age <= 65 else 0.0

    pass


class TableTemporaire60:
    def __init__(self, personne: Personne | Enfant | Conjoint | Ascendant):
        """

        :param personne: La victime
        """
        self.personne = personne

        self.__baremes_masculin: list[float] = \
            [14.425, 14.745, 14.739, 14.715, 14.684, 14.648, 14.609, 14.566, 14.519, 14.470,
             14.417, 14.360, 14.299, 14.235, 14.167, 14.095, 14.022, 13.945, 13.867, 13.785,
             13.700, 13.610, 13.515, 13.415, 13.309, 13.196, 13.077, 12.950, 12.814, 12.670,
             12.517, 12.355, 12.184, 12.004, 11.813, 11.612, 11.399, 11.175, 10.938, 10.688,
             10.423, 10.144, 9.850, 9.538, 9.209, 8.861, 8.493, 8.103, 7.690, 7.252,
             6.787, 6.294, 5.769, 5.210, 4.613, 3.975, 3.293, 2.560, 1.772, 0.921,
             0.000]  # Les barêmes

        self.__baremes_feminin: list[float] = \
            [14.606, 14.848, 14.845, 14.825, 14.798, 14.768, 14.734, 14.697, 14.658, 14.615,
             14.569, 14.519, 14.467, 14.411, 14.352, 14.290, 14.224, 14.155, 14.083, 14.006,
             13.925, 13.840, 13.749, 13.652, 13.550, 13.441, 13.326, 13.204, 13.074, 12.937,
             12.791, 12.637, 12.473, 12.299, 12.113, 11.917, 11.709, 11.487, 11.252, 11.003,
             10.738, 10.457, 10.158, 9.841, 9.505, 9.148, 8.768, 8.365, 7.937, 7.482,
             6.998, 6.483, 5.936, 5.353, 4.731, 4.069, 3.361, 2.605, 1.797, 0.930,
             0.000]  # Les barêmes

    def bareme(self) -> float:
        """
        Par coïncidence les indexe de la liste des barêmes vont de 0 à 100, il suffit juste de retourner le barême situé
        à indexer équivalent en âge à l'âge de la Personnene.
        :return : Le barême correspondant à l'âge de la Personnene
        """
        baremes: list[float] = self.__baremes_feminin if self.personne.sexe == "F" else self.__baremes_masculin
        return baremes[self.personne.age] if 0 <= self.personne.age <= 60 else 0.0
    pass


class TableTemporaire55:
    def __init__(self, personne: Personne | Enfant | Conjoint | Ascendant):
        """

        :param personne: La victime
        """
        self.personne = personne

        self.__baremes_masculin: list[float] = \
            [14.322, 14.633, 14.620, 14.588, 14.548, 14.503, 14.454, 14.401, 14.344, 14.283,
             14.218, 14.148, 14.073, 13.994, 13.910, 13.822, 13.730, 13.635, 13.536 ,13.432,
             13.324, 13.209, 13.088, 12.959, 12.822, 12.677, 12.523, 12.359, 12.184, 11.998,
             11.800, 11.590, 11.368, 11.132, 10.883, 10.618, 10.338, 10.042, 9.728, 9.394,
             9.041, 8.667, 8.269, 7.847, 7.399, 6.923, 6.417, 5.878, 5.303, 4.691,
             4.037, 3.339, 2.591, 1.789, 0.927, 0.000]  # Les barêmes

        self.__baremes_feminin: list[float] = \
            [14.490, 14.723, 14.712, 14.683, 14.647, 14.606, 14.562, 14.514, 14.462, 14.407,
             14.347, 14.283, 14.215, 14.143, 14.067, 13.986, 13.900, 13.810, 13.715, 13.614,
             13.508, 13.394, 13.274, 13.146, 13.011, 12.867, 12.714, 12.551, 12.379, 12.196,
             12.001, 11.794, 11.575, 11.341, 11.092, 10.828, 10.547, 10.249, 9.931, 9.594,
             9.235, 8.853, 8.447, 8.015, 7.555, 7.066, 6.546, 5.991, 5.401, 4.772,
             4.101, 3.385, 2.622, 1.806, 0.933, 0.000]  # Les barêmes

    def bareme(self) -> float:
        """
        Par coïncidence les indexe de la liste des barêmes vont de 0 à 100, il suffit juste de retourner le barême situé
        à indexer équivalent en âge à l'âge de la Personnene.
        :return : Le barême correspondant à l'âge de la Personnene
        """
        baremes: list[float] = self.__baremes_feminin if self.personne.sexe == "F" else self.__baremes_masculin
        return baremes[self.personne.age] if 0 <= self.personne.age <= 55 else 0.0
    pass


class TableTemporaire25:
    def __init__(self, personne: Personne | Enfant | Conjoint | Ascendant):
        """

        :param personne: La victime
        """
        self.personne = personne

        self.__baremes_masculin: list[float] = \
            [11.815, 11.896, 11.698, 11.473, 11.228, 10.965, 10.684, 10.384, 10.064, 9.723,
             9.359, 8.971, 8.558, 8.118, 7.650, 7.151, 6.621, 6.057, 5.457, 4.819,
             4.139, 3.414, 2.641, 1.816, 0.938, 0.000]  # Les barêmes

        self.__baremes_feminin: list[float] = \
            [11.908, 11.920, 11.721, 11.495, 11.249, 10.986, 10.705, 10.405, 10.085, 9.743,
             9.379, 8.991, 8.578, 8.138, 7.670, 7.171, 6.640, 6.074, 5.472, 4.831,
             4.148, 3.420, 2.645, 1.819, 0.938, 0.000]  # Les barêmes

    def bareme(self) -> float:
        """
        Par coïncidence les indexe de la liste des barêmes vont de 0 à 100, il suffit juste de retourner le barême situé
        à indexer équivalent en âge à l'âge de la Personnene.
        :return : Le barême correspondant à l'âge de la Personnene
        """
        baremes: list[float] = self.__baremes_feminin if self.personne.sexe == "F" else self.__baremes_masculin
        return baremes[self.personne.age] if 0 <= self.personne.age <= 25 else 0.0
    pass


class TableTemporaire21:
    def __init__(self, personne: Personne | Enfant | Conjoint | Ascendant):
        """

        :param personne: La victime
        """
        self.personne = personne

        self.__baremes_masculin: list[float] = \
            [10.941, 10.942, 10.680, 10.387, 10.071, 9.732, 9.370, 8.984, 8.573, 8.134,
             7.666, 7.167, 6.636, 6.070, 5.468, 4.826, 4.143, 3.416, 2.642, 1.817,
             0.938, 0.000]  # Les barêmes

        self.__baremes_feminin: list[float] = \
            [11.022, 10.959, 10.696, 10.401, 10.084, 9.745, 9.383, 8.996, 8.584, 8.144,
             7.676, 7.177, 6.645, 6.079, 5.476, 4.834, 4.150, 3.421, 2.646, 1.819,
             0.938, 0.000]  # Les barêmes

    def bareme(self) -> float:
        """
        Par coïncidence les indexe de la liste des barêmes vont de 0 à 100, il suffit juste de retourner le barême situé
        à l'index équivalent en âge à l'âge de la Personnene.
        :return : Le barême correspondant à l'âge de la Personnene
        """
        baremes: list[float] = self.__baremes_feminin if self.personne.sexe == "F" else self.__baremes_masculin
        return baremes[self.personne.age] if 0 <= self.personne.age <= 21 else 0.0
    pass


class NiveauPrejudice:
    def __init__(self):
        pass

    @property
    def tres_leger(self) -> int:
        return 5

    @property
    def leger(self) -> int:
        return 10

    @property
    def modere(self) -> int:
        return 20

    @property
    def moyen(self) -> int:
        return 40

    @property
    def assez_important(self) -> int:
        return 60

    @property
    def important(self) -> int:
        return 100

    @property
    def tres_important(self) -> int:
        return 150

    @property
    def exceptionnel(self) -> int:
        return 300


class ValeurPointIP:
    def __init__(self, person: Personne, taux_ip: float):
        """

        :param person: La victime
        :param taux_ip: Le taux d'IP
        """
        self.person: Personne = person
        self.taux_ip: float = taux_ip

        self.age: int = self.person.age

    @property
    def valeur(self):

        if self.person.age <= 0:
            return 0

        if self.taux_ip <= 5:
            if self.person.age <= 59:
                return 6
            else:
                return 5

        if self.taux_ip <= 10:
            if self.person.age <= 59:
                return 12
            else:
                return 10

        if self.taux_ip <= 15:
            if self.person.age <= 39:
                return 14
            elif self.person.age <= 59:
                return 12
            else:
                return 10

        if self.taux_ip <= 20:
            if self.person.age <= 19:
                return 16
            elif self.person.age <= 39:
                return 14
            else:
                return 12

        if self.taux_ip <= 30:
            if self.person.age <= 19:
                return 17
            elif self.person.age <= 39:
                return 17
            elif self.person.age <= 69:
                return 17
            else:
                return 12

        if self.taux_ip <= 40:
            if self.person.age <= 19:
                return 18
            elif self.person.age <= 29:
                return 17
            elif self.person.age <= 39:
                return 16
            elif self.person.age <= 69:
                return 14
            else:
                return 13

        if self.taux_ip <= 50:
            if self.person.age <= 24:
                return 18
            elif self.person.age <= 39:
                return 17
            elif self.person.age <= 59:
                return 16
            elif self.person.age <= 69:
                return 15
            else:
                return 13

        if self.taux_ip <= 70:
            if self.person.age <= 24:
                return 19
            elif self.person.age <= 39:
                return 18
            elif self.person.age <= 59:
                return 17
            elif self.person.age <= 69:
                return 16
            else:
                return 14

        if self.taux_ip <= 90:
            if self.person.age <= 15:
                return 25
            elif self.person.age <= 24:
                return 20
            elif self.person.age <= 39:
                return 19
            elif self.person.age <= 59:
                return 18
            elif self.person.age <= 69:
                return 17
            else:
                return 15

        if self.taux_ip <= 100:
            if self.person.age <= 15:
                return 29
            elif self.person.age <= 24:
                return 24
            elif self.person.age <= 39:
                return 22
            elif self.person.age <= 59:
                return 20
            elif self.person.age <= 69:
                return 19
            else:
                return 18

        return -1

    pass


class SituationMatrimoniale:
    CELIBATAIRE = "Célibataire"
    MARIE_E = "Marié.e"
    DIVORCE = "Divorcé.e"
    VEUF_VE = "Veuf/Veuve"


class Repartition(ABC):
    def __init__(self):
        self.ascendants: int = 0
        self.conjoints: int = 0
        self.enfants: int = 0
        self.enfants_orphelins_double: int = 0

        self.repartition() # On appelle la fonction qui met à jour les différentes valeurs.
        # Il s'agit d'une méthode à implémenter dans la classe héritant de celle-ci présente alors classe parente.

    @abstractmethod
    def repartition(self):
        pass
    pass

