import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QMessageBox

from algorithm.dead import PrejudiceEconomiqueConjoints, ControlePlafondPrejudiceEconomique, PrejudiceEconomiqueEnfants,\
    PrejudiceMoral, ControlePlafondPrejudiceMoral
from algorithm.profils import Enfant, Conjoint, Personne, Ascendant, Collateral

from algorithm.tables import SituationMatrimoniale


app = QApplication(sys.argv)

from database_manager import personnes, rechercher_personne_par_id


class CustomAyantsDroitsList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(700)
        self.setMinimumHeight(110)
        self.setStyleSheet("""
                                    QListWidget {
                                        background: qlineargradient(
                                            x1: 0, y1: 0,
                                            x2: 1, y2: 1,
                                            stop: 0 #1f1f4d,
                                            stop: 0.6 #2f2ca0,
                                            stop: 1 #3131b8
                                        );
                                        border: none;  /* Supprime toute bordure visible */
                                        border-radius: 8px;
                                        padding: 6px;
                                        color: #f0f3ff;
                                        font-weight: 500;
                                    }

                                    QListWidget::item {
                                        background-color: transparent;
                                        padding: 8px 14px;
                                        border: none;
                                        border-bottom: 1px solid rgba(240, 240, 240, 0.05);
                                    }

                                    QListWidget::item:hover {
                                        background-color: rgba(255, 255, 255, 0.05);
                                    }

                                    QListWidget::item:selected {
                                        background-color: rgba(255, 255, 255, 0.12);
                                        color: #e3f3ff;
                                        border-left: 3px solid #5B95D6;
                                    }

                                    QScrollBar:vertical {
                                        background: transparent;
                                        width: 6px;
                                        margin: 0px;
                                        padding: 0px;
                                        border: none;
                                    }

                                    QScrollBar::handle:vertical {
                                        background: #5B95D6;
                                        border-radius: 3px;
                                        min-height: 20px;
                                    }

                                    QScrollBar::add-line:vertical,
                                    QScrollBar::sub-line:vertical {
                                        height: 0px;
                                        background: none;
                                    }

                                    QScrollBar::add-page:vertical,
                                    QScrollBar::sub-page:vertical {
                                        background: none;
                                    }

                                """)


class LoadList:
    def __init__(self, list_view_widget, list_to_load):
        self.list_to_load = list_to_load
        self.list_widget = list_view_widget

    def load_list(self, list_to_load):

        try:

            attr = ["nom", "prenom", "age", "sexe"]
            if not list_to_load:
                return

            for individu in list_to_load:
                informations = []
                for attribute in attr:
                    # Utiliser getattr avec valeur par défaut None, puis filtrer
                    value = getattr(individu, attribute, None)
                    if value is not None:
                        informations.append(str(value))

                # Joindre seulement les attributs existants
                self.list_widget.addItem(" ".join(informations))
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Une erreur s'est produite :\n{str(e)}")

    def reload(self, list_to_reload):
        self.list_widget.clear()
        self.load_list(list_to_load=list_to_reload)
    pass


class ListVictime(CustomAyantsDroitsList):
    def __init__(self):
        super().__init__()

        self.liste_personnes = personnes()

        for personne in self.liste_personnes:
            self.addItem(f"{personne.id} - {personne.nom} - {personne.prenom} - {personne.sexe}")

        self.personne = rechercher_personne_par_id(1)  # Par défaut la première personne.

    pass


class ListEnfants(CustomAyantsDroitsList):
    def __init__(self, personne: Personne):
        self.personne = personne
        super().__init__()
        self.loader = LoadList(list_view_widget=self, list_to_load=self.personne.enfants)
    pass


class ListConjoints(CustomAyantsDroitsList):
    def __init__(self, personne: Personne):
        self.personne = personne
        super().__init__()
        self.loader = LoadList(list_view_widget=self, list_to_load=self.personne.conjoints)
    pass


class ListCollateraux(CustomAyantsDroitsList):
    def __init__(self, personne: Personne):
        self.personne = personne
        super().__init__()
        self.loader = LoadList(list_view_widget=self, list_to_load=self.personne.collateraux)
    pass


class ListAscendants(CustomAyantsDroitsList):
    def __init__(self, personne: Personne):
        self.personne = personne
        super().__init__()
        self.loader = LoadList(list_view_widget=self, list_to_load=self.personne.ascendants)
    pass


class ListAyantsDroit(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        self.__list_vitimes = ListVictime()
        self.__list_enfants = ListEnfants(self.__list_vitimes.personne)
        self.__list_conjoints = ListConjoints(self.__list_vitimes.personne)
        self.__list_ascendants = ListAscendants(self.__list_vitimes.personne)
        self.__list_collateraux = ListCollateraux(self.__list_vitimes.personne)

        # self.__list_vitimes.itemDoubleClicked.connect(self.__item_double_clicked) # Le double click
        # servira à charger les données.
        self.__list_vitimes.itemPressed.connect(self.__item_double_clicked)

        label_list_personnes = QLabel("Listes des victimes")
        label_list_enfants = QLabel("Enfants de la victime")
        label_list_conjoints = QLabel("Conjoints de la victime")
        label_list_ascendants = QLabel("Parents de la victime")
        label_list_collateraux = QLabel("Frères et soeur de la victime")

        for lbl in [label_list_personnes,
                    label_list_collateraux,
                    label_list_conjoints,
                    label_list_ascendants,
                    label_list_enfants]:
            lbl.setStyleSheet("""
                        background-color: transparent;
                        font-weight: bold;
                        color: #31588A;
                        margin-bottom: 3px;
                        font-size: 14px;
                            """)
            lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        widgets = [label_list_personnes,
                   self.__list_vitimes,
                   label_list_enfants,
                   self.__list_enfants,
                   label_list_conjoints,
                   self.__list_conjoints,
                   label_list_ascendants,
                   self.__list_ascendants,
                   label_list_collateraux,
                   self.__list_collateraux,
                   ]

        for widget in widgets:
            self.main_layout.addWidget(widget)

    def __item_double_clicked(self, item):
        print(f"Index sélectionné: {self.__list_vitimes.row(item)}")

        # Récupération de l'index (avec vérification)
        selected_row = self.__list_vitimes.row(item)
        if selected_row < 0:
            print("Aucun élément sélectionné")
            return

        self.personne = rechercher_personne_par_id(selected_row + 1)
        print("=====================================================================")
        print(self.personne.nom, self.personne.prenom, self.personne.sexe, self.personne.age)

        # Accès direct aux relations maintenant chargées
        print("=====================================================================")
        print("Enfants:")
        for enfant in self.personne.enfants:
            print(f"  - {enfant.prenom} {enfant.nom} ({enfant.age} ans)")

        print("Conjoints:")
        for conjoint in self.personne.conjoints:
            print(f"  - {conjoint.prenom} {conjoint.nom} ({conjoint.age} ans)")

        try:
            self.__list_enfants.loader.reload(self.personne.enfants)
            self.__list_conjoints.loader.reload(self.personne.conjoints)
            self.__list_ascendants.loader.reload(self.personne.ascendants)
            self.__list_collateraux.loader.reload(self.personne.collateraux)
        except:
            # Message d'avertissement
            QMessageBox.warning(None, "Attention", "Ceci est un avertissement!")
        finally:
            pass # Ne pas fermer la fenêtre.



main_window = QWidget()
main_window.setStyleSheet("""background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #B9D5F9,
        stop:0.6 #e8f2ff,
        stop:1 #d0e3ff
    );""")
main_layout = QHBoxLayout(main_window)
main_layout.addWidget(ListAyantsDroit())
main_window.show()

if __name__ == '__main__':
    sys.exit(app.exec())