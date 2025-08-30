import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QMessageBox, QDialog, \
    QGridLayout, QLineEdit, QComboBox, QStackedLayout, QListView, QStackedWidget, QCheckBox, QPushButton, QMenu

from algorithm.dead import PrejudiceEconomiqueConjoints, ControlePlafondPrejudiceEconomique, PrejudiceEconomiqueEnfants,\
    PrejudiceMoral, ControlePlafondPrejudiceMoral
from algorithm.profils import Enfant, Conjoint, Personne, Ascendant, Collateral

from algorithm.tables import SituationMatrimoniale, AGE_LIMITE, list_pays_cima
from database_manager import ajouter_personne_data_base, supprimer_et_reorganiser_ids
from api import data_contoller


app = QApplication(sys.argv)

# Données de test

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


class ModifierProfil(QDialog):
    def __init__(self, personne: Personne | None, personne_indexe: int = 0):
        super().__init__()


        if personne is None:
            personne_ = Personne(
                        nom="",
                        prenom="",
                        age=00,
                        sexe="M",
                        profession="",
                        salaire=0,
                        age_limite=60,
                        situation_matrimoniale=SituationMatrimoniale.CELIBATAIRE,
                        conjoints=[],
                        enfants=[],
                        ascendants=[],
                        collateraux=[],
                        pays_residence="Togo",
                        pays_sinistre="Togo",
                    )
            self.personne = personne_
            self.modification = False

            if data_contoller.load_profil_alive:
                data_contoller.call_fonction(key="close_profil_alive")
            else:
                data_contoller.call_fonction(key="close_profil_dead")
        else:
            self.personne = personne
            self.modification = True
            self.personne_index = personne_indexe

        self.enfants = self.personne.enfants
        self.conjoints = self.personne.conjoints
        self.ascendants = self.personne.ascendants
        self.collateraux = self.personne.collateraux

        self.list_view_enfant = QListWidget()
        self.list_view_conjoint = QListWidget()
        self.list_view_ascendant = QListWidget()
        self.list_view_collateral = QListWidget()

        self.main_layout = QVBoxLayout(self)
        self.setStyleSheet("""
                    QLabel {
                        color: #31588A;
                        margin-bottom: 3px;
                        font-size: 14px;
                    }

                    QWidget {
                        background-color: transparent;
                    }

                    QLineEdit {
                        background-color: qlineargradient(
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 #99C0F1,
                            stop:0.6 #B3CAE9,
                            stop:1 #ADC8F1);
                        color: #060270;
                        border-radius: 5px;
                        font-size: 15; font-weight: bold;
                        margin-bottom: 7px;
                        padding: 5px 10px 5px 5px;  /* Top, Right, Bottom, Left */
                    }

                    QCheckBox {
                        background-color: qlineargradient(
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 #99C0F1,
                            stop:0.6 #B3CAE9,
                            stop:1 #ADC8F1);
                        font-size: 18; font-weight: bold; color: #31588A;
                        border: 1px solid #7A9CC6;
                        margin-bottom: 7px;
                        padding: 5px 10px 5px 5px;
                    }


                    QComboBox {
                        background-color: qlineargradient(
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 #99C0F1,
                            stop:0.6 #B3CAE9,
                            stop:1 #ADC8F1);
                        color: #060270;
                        border-radius: 5px;
                        font-size: 15px; 
                        font-weight: bold;
                        border: 1px solid #7A9CC6;
                        margin-bottom: 7px;
                        padding: 5px 10px 5px 5px;
                        min-width: 100px;
                    }

                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 40px;
                        border-left: 1px solid #7A9CC6;
                        border-top-right-radius: 5px;
                        border-bottom-right-radius: 5px;
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 #99C0F1,
                            stop:0.6 #B3CAE9,
                            stop:1 #ADC8F1);
                    }

                    QComboBox::down-arrow {
                        image: url(assets/icons8-box-move-down-32-2.png);
                        width: 12px;
                        height: 12px;
                    }

                    QComboBox:hover {
                        border: 1px solid #4A7CBF;
                    }

                    QComboBox:on {
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 #89B0E1,
                            stop:1 #9DB8E1);
                        color: #060270;
                    }

                    QComboBox:disabled {
                        background: #D3D3D3;
                        color: #808080;
                    }

                    /* [MODIFICATIONS UNIQUEMENT ICI] */
                    QComboBox QAbstractItemView {
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 #99C0F1,
                            stop:0.6 #B3CAE9,
                            stop:1 #ADC8F1);
                        color: #060270;
                        selection-background-color: #4A7CBF;
                        selection-color: white;  /* Changé pour meilleure lisibilité */
                        border: 1px solid #7A9CC6;
                        border-radius: 5px;
                        outline: none;
                        font-size: 14px;
                        padding: 4px;
                    }

                    /* Style des items au survol */
                    QComboBox QAbstractItemView::item:hover {
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 #7A9CC6,
                            stop:1 #4A7CBF);
                        color: white;
                        font-weight: bold;
                    }

                    /* Style des items sélectionnés au survol */
                    QComboBox QAbstractItemView::item:selected:hover {
                        background: #2A5C8B;
                        color: white;
                    } 
                    
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


        label_entete = QLabel("Modification du profil")
        label_entete.setStyleSheet("""
                            QLabel {
                                color: #34495e;
                                font-size: 16px;
                                font-weight: 600;
                                padding-bottom: 8px;
                                border-bottom: 2px solid #3498db;  /* Ligne de séparation bleue */
                                margin-bottom: 15px;
                            }
                        """)
        label_entete.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(label_entete)

        # La layout formulaire de la victime
        formulaire_layout = QGridLayout()
        self.main_layout.addLayout(formulaire_layout)
        
        self.profil_nom_le = QLineEdit()
        self.profil_prenom_le = QLineEdit()
        self.profil_age_le = QLineEdit()

        self.profil_profession_le = QLineEdit()
        self.profil_salaire_le = QLineEdit()
        self.profil_matrimoniale_cb = QComboBox()

        self.profil_pays_residence_cb = QComboBox()
        self.profil_pays_sinistre_cb = QComboBox()
        self.profil_sexe_cb = QComboBox()

        self.profil_sexe_cb.addItems(["M", "F"])
        self.profil_matrimoniale_cb.addItems([SituationMatrimoniale.CELIBATAIRE,
                                              SituationMatrimoniale.MARIE_E,
                                              SituationMatrimoniale.DIVORCE,
                                              SituationMatrimoniale.VEUF_VE])
        self.profil_pays_residence_cb.addItems(list_pays_cima)
        self.profil_pays_sinistre_cb.addItems(list_pays_cima)

        # Définition des valeurs par défauts
        self.profil_nom_le.setText(self.personne.nom)
        self.profil_prenom_le.setText(self.personne.prenom)
        self.profil_age_le.setText(f"{self.personne.age}")
        self.profil_profession_le.setText(self.personne.profession)
        self.profil_salaire_le.setText(f"{self.personne.salaire}")
        self.profil_matrimoniale_cb.setCurrentText(self.personne.situation_matrimoniale)
        self.profil_sexe_cb.setCurrentText(self.personne.sexe)
        self.profil_pays_residence_cb.setCurrentText(self.personne.pays_residence)
        self.profil_pays_sinistre_cb.setCurrentText(self.personne.pays_sinistre)

        #~Mise en place des widgets pour le profil de la victime.
        column = 0
        for label in [QLabel("Nom :"), QLabel("Prénom :"), QLabel("Age :")]:
            formulaire_layout.addWidget(label, 0, column)
            column += 1

        column = 0
        for entry in [self.profil_nom_le, self.profil_prenom_le, self.profil_age_le]:
            formulaire_layout.addWidget(entry, 1, column)
            column += 1

        column = 0
        for label in [QLabel("Profession :"), QLabel("Salaire / Bourse mensuelle :"),
                      QLabel("Situation matrimoniale :")]:
            formulaire_layout.addWidget(label, 2, column)
            column += 1

        column = 0
        for entry in [self.profil_profession_le, self.profil_salaire_le,
                      self.profil_matrimoniale_cb]:
            formulaire_layout.addWidget(entry, 3, column)
            column += 1

        column = 0
        for label in [QLabel("Pays de résidence :"), QLabel("Pays lieu du sinistre :"), QLabel("Sexe :")]:
            formulaire_layout.addWidget(label, 4, column)
            column += 1

        column = 0
        for entry in [self.profil_pays_residence_cb, self.profil_pays_sinistre_cb,
                      self.profil_sexe_cb]:
            formulaire_layout.addWidget(entry, 5, column)
            column += 1

        # Parties des ayants droit.
        label_entete = QLabel("Les ayants droit")
        label_entete.setStyleSheet("""
                                    QLabel {
                                        color: #34495e;
                                        font-size: 16px;
                                        font-weight: 600;
                                        padding-bottom: 8px;
                                        border-bottom: 2px solid #3498db;  /* Ligne de séparation bleue */
                                        margin-bottom: 15px;
                                    }
                                """)
        label_entete.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(label_entete)

        ayants_label_layout = QHBoxLayout()
        self.main_layout.addLayout(ayants_label_layout)

        ayants_label_layout.addWidget(QLabel("Choisir les ayants droit à afficher : "))
        ayant_droit_types = QComboBox()
        ayant_droit_types.addItems(["Ascendants", "Collatéraux", "Conjoints", "Enfants/Descants"])
        ayant_droit_types.currentTextChanged.connect(self.update_list_view)
        ayants_label_layout.addWidget(ayant_droit_types)

        # Ajout d'un autre layout pour l'affichage et la modification des réusltats.
        result_lit_layout = QHBoxLayout()
        self.main_layout.addLayout(result_lit_layout)

        # Utilisation d'une stack layout pour l'affichage des listes.
        self.list_view_widget = QStackedWidget()
        result_lit_layout.addWidget(self.list_view_widget)

        self.ascendants_list = QListWidget(); self.ascendats_layout = QVBoxLayout()
        self.collateraux_list = QListWidget(); self.collateraux_layout = QVBoxLayout()
        self.conjoints_list = QListWidget(); self.conjoints_layout = QVBoxLayout()
        self.enfants_list = QListWidget(); self.enfants_layout = QVBoxLayout()

        # Insertion des données.
        for ascendant in self.personne.ascendants:
            self.ascendants_list.addItem(f"Nom : {ascendant.nom}\nPrénom : {ascendant.prenom}\n Age : {ascendant.age} ans\nSexe: {ascendant.sexe}")

        for conjoint in self.personne.conjoints:
            self.conjoints_list.addItem(f"Nom : {conjoint.nom}\nPrénom : {conjoint.prenom}\nAge : {conjoint.age} ans\nSexe: {conjoint.sexe}")

        for individu in self.personne.enfants:
            self.enfants_list.addItem(f"Nom : {individu.nom} \nPrénom : {individu.prenom} \nAge: {individu.age} ans \nSexe : {individu.sexe} \nPoursuit les études : {"Oui" if individu.poursuit_etudes else "Non"} \nHandicap majeur à vie : {"Oui" if individu.handicap_majeur else "Non"}")

        for collateral in self.personne.collateraux:
            self.collateraux_list.addItem(f"Nom : {collateral.nom}\nAge : {collateral.prenom}\nSexe : {collateral.age} ans")

        # Ajout des layouts enfants.
        for widget in [self.ascendants_list, self.collateraux_list, self.conjoints_list, self.enfants_list]:
            self.list_view_widget.addWidget(widget)

        self.list_view_widget.setCurrentWidget(self.ascendants_list)

        # Ajout d'une QGridLayout pour les données modifiables.
        data_grid_layout = QGridLayout()
        result_lit_layout.addLayout(data_grid_layout)

        self.nouveau_nom = QLineEdit()
        self.nouveau_prenom = QLineEdit()
        self.nouvel_age = QLineEdit()

        self.nouveau_sexe = QComboBox()
        self.nouveau_sexe.addItems(["M", "F"])
        self.nouveau_etudes = QCheckBox("Poursuit les études.")
        self.nouveau_handicap_majeur = QCheckBox("Handicap majeur.")

        self.nouveau_orphelin_double = QCheckBox("Orphelin double.")

        data_grid_layout.addWidget(QLabel("Nom :"), 0, 0)
        data_grid_layout.addWidget(QLabel("Prénom :"), 0, 1)

        data_grid_layout.addWidget(self.nouveau_nom, 1, 0)
        data_grid_layout.addWidget(self.nouveau_prenom, 1, 1)

        data_grid_layout.addWidget(QLabel("Age :"), 2, 0)
        data_grid_layout.addWidget(QLabel("Sexe :"), 2, 1)

        data_grid_layout.addWidget(self.nouvel_age, 3, 0)
        data_grid_layout.addWidget(self.nouveau_sexe, 3, 1)

        data_grid_layout.addWidget(self.nouveau_etudes, 4, 0, 1, 2)
        data_grid_layout.addWidget(self.nouveau_handicap_majeur, 5, 0, 1, 2)
        data_grid_layout.addWidget(self.nouveau_orphelin_double, 6, 0, 1, 2)

        self.nouveau_etudes.setDisabled(True)
        self.nouveau_handicap_majeur.setDisabled(True)
        self.nouveau_orphelin_double.setDisabled(True)

        self.type__ = "Ascendant"

        self.ajouter_individu_but = QPushButton("➕Ajouter")
        self.ajouter_individu_but.setStyleSheet("""
                                                QPushButton {
                                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 #2EA44F,       /* Vert GitHub vif */
                                                        stop:1 #22863A);      /* Vert GitHub foncé */
                                                    border: 1px solid #2EA44F;
                                                    border-radius: 6px;
                                                    color: white;             /* Texte blanc */
                                                    font-weight: 600;         /* Gras moyen */
                                                    padding: 5px;
                                                    font-size: 12px;
                                                }

                                                QPushButton:hover {
                                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 #34D058,       /* Vert GitHub clair (survol) */
                                                        stop:1 #28A745);     /* Vert GitHub moyen */
                                                    border-color: #34D058;
                                                }

                                                QPushButton:pressed {
                                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 #22863A,      /* Vert foncé */
                                                        stop:1 #176F2C);     /* Vert très foncé */
                                                }
                                            """)
        self.ajouter_individu_but.clicked.connect(lambda : self.ajouter_individu(self.type_))
        data_grid_layout.addWidget(self.ajouter_individu_but, 7, 0, 1, 2)

        self.validate_but = QPushButton("💾Enregistrer les modifications")
        self.validate_but.setFixedWidth(253)
        self.validate_but.setStyleSheet("""
                                                QPushButton {
                                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 #0366d6,       /* Bleu GitHub vif */
                                                        stop:1 #035fc7);      /* Bleu GitHub foncé */
                                                    border: 1px solid #0366d6;
                                                    border-radius: 6px;
                                                    color: white;             /* Texte blanc */
                                                    font-weight: 600;         /* Gras moyen */
                                                    padding: 5px;
                                                    font-size: 12px;
                                                }

                                                QPushButton:hover {
                                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 #1384ff,       /* Bleu GitHub clair (survol) */
                                                        stop:1 #0374e8);      /* Bleu GitHub moyen */
                                                    border-color: #1384ff;
                                                }

                                                QPushButton:pressed {
                                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 #035fc7,       /* Bleu foncé */
                                                        stop:1 #0255b3);      /* Bleu très foncé */
                                                }
                                            """)
        self.main_layout.addWidget(self.validate_but)


        self.ascendants_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # Pour le click contextuel.
        self.collateraux_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # Pour le click contextuel.
        self.conjoints_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # Pour le click contextuel.
        self.enfants_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # Pour le click contextuel.

        # Connecter le signal de menu contextuel
        self.ascendants_list.customContextMenuRequested.connect(self.supprimer_ascendant)
        self.enfants_list.customContextMenuRequested.connect(self.supprimer_enfant)
        self.conjoints_list.customContextMenuRequested.connect(self.supprimer_conjoint)
        self.collateraux_list.customContextMenuRequested.connect(self.supprimer_collateral)

    @property
    def type_(self):
        return self.type__

    @type_.setter
    def type_(self, type_: str):
        self.type__ = type_


    def update_list_view(self, value):
        match value:
            case "Ascendants":
                self.list_view_widget.setCurrentWidget(self.ascendants_list)

                self.nouveau_etudes.setDisabled(True)
                self.nouveau_handicap_majeur.setDisabled(True)
                self.nouveau_orphelin_double.setDisabled(True)
                self.nouveau_sexe.setDisabled(False)
                self.type_ = "Ascendant"

            case "Enfants/Descants":
                self.list_view_widget.setCurrentWidget(self.enfants_list)

                self.nouveau_etudes.setDisabled(False)
                self.nouveau_handicap_majeur.setDisabled(False)
                self.nouveau_orphelin_double.setDisabled(False)
                self.nouveau_sexe.setDisabled(False)
                self.type_ = "Enfant"

            case "Conjoints":
                self.list_view_widget.setCurrentWidget(self.conjoints_list)

                self.nouveau_etudes.setDisabled(True)
                self.nouveau_handicap_majeur.setDisabled(True)
                self.nouveau_orphelin_double.setDisabled(True)
                self.nouveau_sexe.setDisabled(False)
                self.type_ = "Conjoint"

            case "Collatéraux":
                self.list_view_widget.setCurrentWidget(self.collateraux_list)

                self.nouveau_etudes.setDisabled(True)
                self.nouveau_handicap_majeur.setDisabled(True)
                self.nouveau_orphelin_double.setDisabled(True)
                self.nouveau_sexe.setDisabled(True)
                self.type_ = "Collatéral"

        pass

    def supprimer_enfant(self, position):

        index = self.enfants_list.indexAt(position)

        if not index.isValid():
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
        /* Style léger pour le menu contextuel */
            QMenu {
                background-color: white;
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 4px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                font-size: 13px;
            }

            QMenu::item {
                padding: 6px 12px;
                border-radius: 4px;
                margin: 2px;
                color: #24292f;
            }

            QMenu::item:selected {
                background-color: #0969da;
                color: white;
            }

            QMenu::item:disabled {
                color: #8c959f;
            }

            QMenu::separator {
                height: 1px;
                background-color: #d0d7de;
                margin: 4px 0;
            }
        """)

        action_modifier = QAction("🚮Supprimer", self)
        menu.addAction(action_modifier)
        try:
            print(index.row())
            action_modifier.triggered.connect(lambda : self.__action_supprimer_enfant(index.row()))
        except Exception as e:
            print(e)

        menu.exec(self.enfants_list.mapToGlobal(position))
        pass

    def supprimer_conjoint(self, position):

        index = self.conjoints_list.indexAt(position)

        if not index.isValid():
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
        /* Style léger pour le menu contextuel */
            QMenu {
                background-color: white;
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 4px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                font-size: 13px;
            }

            QMenu::item {
                padding: 6px 12px;
                border-radius: 4px;
                margin: 2px;
                color: #24292f;
            }

            QMenu::item:selected {
                background-color: #0969da;
                color: white;
            }

            QMenu::item:disabled {
                color: #8c959f;
            }

            QMenu::separator {
                height: 1px;
                background-color: #d0d7de;
                margin: 4px 0;
            }
        """)

        action_modifier = QAction("🚮Supprimer", self)
        action_modifier.triggered.connect(lambda : self.__action_supprimer_conjoint(index.row()))
        menu.addAction(action_modifier)

        menu.exec(self.conjoints_list.mapToGlobal(position))
        pass

    def supprimer_ascendant(self, position):

        index = self.ascendants_list.indexAt(position)

        if not index.isValid():
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
        /* Style léger pour le menu contextuel */
            QMenu {
                background-color: white;
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 4px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                font-size: 13px;
            }

            QMenu::item {
                padding: 6px 12px;
                border-radius: 4px;
                margin: 2px;
                color: #24292f;
            }

            QMenu::item:selected {
                background-color: #0969da;
                color: white;
            }

            QMenu::item:disabled {
                color: #8c959f;
            }

            QMenu::separator {
                height: 1px;
                background-color: #d0d7de;
                margin: 4px 0;
            }
        """)

        action_modifier = QAction("🚮Supprimer", self)
        action_modifier.triggered.connect(lambda : self.__action_supprimer_ascendant(index.row()))
        menu.addAction(action_modifier)

        menu.exec(self.ascendants_list.mapToGlobal(position))
        pass

    def supprimer_collateral(self, position):

        index = self.collateraux_list.indexAt(position)

        if not index.isValid():
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
        /* Style léger pour le menu contextuel */
            QMenu {
                background-color: white;
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 4px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                font-size: 13px;
            }

            QMenu::item {
                padding: 6px 12px;
                border-radius: 4px;
                margin: 2px;
                color: #24292f;
            }

            QMenu::item:selected {
                background-color: #0969da;
                color: white;
            }

            QMenu::item:disabled {
                color: #8c959f;
            }

            QMenu::separator {
                height: 1px;
                background-color: #d0d7de;
                margin: 4px 0;
            }
        """)

        action_modifier = QAction("🚮Supprimer", self)
        action_modifier.triggered.connect(lambda : self.__action_supprimer_collateral(index.row()))
        menu.addAction(action_modifier)

        menu.exec(self.collateraux_list.mapToGlobal(position))
        pass

    def __action_supprimer_enfant(self, index):
        self.personne.enfants.pop(index)

        self.enfants_list.clear()
        for individu in self.personne.enfants:
            self.enfants_list.addItem(
                f"Nom : {individu.nom} \nPrénom : {individu.prenom} \nAge: {individu.age} ans \nSexe : {individu.sexe} \nPoursuit les études : {"Oui" if individu.poursuit_etudes else "Non"} \nHandicap majeur à vie : {"Oui" if individu.handicap_majeur else "Non"}")
        pass

    def __action_supprimer_conjoint(self, index):
        self.personne.conjoints.pop(index)

        self.conjoints_list.clear()
        for conjoint in self.personne.conjoints:
            self.conjoints_list.addItem(
                f"Nom : {conjoint.nom}\nPrénom : {conjoint.prenom}\nAge : {conjoint.age} ans\nSexe: {conjoint.sexe}")
        pass

    def __action_supprimer_collateral(self, index):
        self.personne.collateraux.pop(index)

        self.collateraux_list.clear()
        for collateral in self.personne.collateraux:
            self.collateraux_list.addItem(
                f"Nom : {collateral.nom}\nAge : {collateral.prenom}\nSexe : {collateral.age} ans")
        pass

    def __action_supprimer_ascendant(self, index):
        self.personne.ascendants.pop(index)

        self.ascendants_list.clear()
        for ascendant in self.personne.ascendants:
            self.ascendants_list.addItem(
                f"Nom : {ascendant.nom}\nPrénom : {ascendant.prenom}\n Age : {ascendant.age} ans\nSexe: {ascendant.sexe}")
        pass

    def ajouter_individu(self, type_: str):
        match type_:
            case "Ascendant":

                nom = self.nouveau_nom.text()
                prenom = self.nouveau_prenom.text()
                age = self.nouvel_age.text()
                sexe = self.nouveau_sexe.currentText()

                if not nom or not prenom:
                    QMessageBox.critical(None, "Erreur",
                                         f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
                    return

                try:
                    int(age)
                except:
                    QMessageBox.critical(None, "Erreur",
                                         f"L'âge doit être une valeur numérique sans espace.\nEchec de l'enrégistrement.")
                    return

                try:
                    int(age) > 100
                except:
                    QMessageBox.critical(None, "Erreur",
                                         f"L'âge ne saurait être supérieur à 100.\nCe n'est pas prévu par le code CIMA.\nEchec de l'enrégistrement.")
                    return

                if (nom, prenom) in [(ascendant.nom, ascendant.prenom) for ascendant in self.personne.ascendants]:
                    return

                ascendant = Ascendant(nom=nom,
                                     prenom=prenom,
                                     age=age,
                                     sexe=sexe)

                self.personne.ascendants.append(ascendant)

                # Réinitialisation de l'affichage.
                self.ascendants_list.clear()
                for ascendant in self.personne.ascendants:
                    self.ascendants_list.addItem(
                        f"Nom : {ascendant.nom}\nPrénom : {ascendant.prenom}\n Age : {ascendant.age} ans\nSexe: {ascendant.sexe}")
            case "Conjoint":

                nom = self.nouveau_nom.text()
                prenom = self.nouveau_prenom.text()
                age = self.nouvel_age.text()
                sexe = self.nouveau_sexe.currentText()

                if not nom or not prenom:
                    QMessageBox.critical(None, "Erreur",
                                         f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
                    return

                try:
                    int(age)
                except:
                    QMessageBox.critical(None, "Erreur",
                                         f"L'âge doit être une valeur numérique sans espace.\nEchec de l'enrégistrement.")
                    return

                try:
                    int(age) > 100
                except:
                    QMessageBox.critical(None, "Erreur",
                                         f"L'âge ne saurait être supérieur à 100.\nCe n'est pas prévu par le code CIMA.\nEchec de l'enrégistrement.")
                    return

                if (nom, prenom) in [(ascendant.nom, ascendant.prenom) for ascendant in self.personne.conjoints]:
                    return

                conjoint = Conjoint(nom=nom,
                                      prenom=prenom,
                                      age=age,
                                      sexe=sexe)
                self.personne.conjoints.append(conjoint)

                # Réinitialisation de l'affichage.
                self.conjoints_list.clear()
                for conjoint in self.personne.conjoints:
                    self.conjoints_list.addItem(
                        f"Nom : {conjoint.nom}\nPrénom : {conjoint.prenom}\nAge : {conjoint.age} ans\nSexe: {conjoint.sexe}")
            case "Collatéral":

                nom = self.nouveau_nom.text()
                prenom = self.nouveau_prenom.text()
                age = self.nouvel_age.text()

                if not nom or not prenom:
                    QMessageBox.critical(None, "Erreur",
                                         f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
                    return

                try:
                    int(age)
                except:
                    QMessageBox.critical(None, "Erreur",
                                         f"L'âge doit être une valeur numérique sans espace.\nEchec de l'enrégistrement.")
                    return

                try:
                    int(age) > 100
                except:
                    QMessageBox.critical(None, "Erreur",
                                         f"L'âge ne saurait être supérieur à 100.\nCe n'est pas prévu par le code CIMA.\nEchec de l'enrégistrement.")
                    return

                if (nom, prenom) in [(ascendant.nom, ascendant.prenom) for ascendant in self.personne.collateraux]:
                    return

                collateral = Collateral(nom=nom,
                                      prenom=prenom,
                                      age=age)
                self.personne.collateraux.append(collateral)

                # Réinitialisation de l'affichage.
                self.collateraux_list.clear()
                for collateral in self.personne.collateraux:
                    self.collateraux_list.addItem(
                        f"Nom : {collateral.nom}\nAge : {collateral.prenom}\nSexe : {collateral.age} ans")
                print()
            case "Enfant":

                nom = self.nouveau_nom.text()
                prenom = self.nouveau_prenom.text()
                age = self.nouvel_age.text()
                sexe = self.nouveau_sexe.currentText()
                etudes = self.nouveau_etudes.isChecked()
                handicap_majeur = self.nouveau_handicap_majeur.isChecked()
                orpehlin_double = self.nouveau_orphelin_double.isChecked()

                if not nom or not prenom:
                    QMessageBox.critical(None, "Erreur",
                                         f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
                    return

                try:
                    int(age)
                except:
                    QMessageBox.critical(None, "Erreur",
                                         f"L'âge doit être une valeur numérique sans espace.\nEchec de l'enrégistrement.")
                    return

                try:
                    int(age) > 100
                except:
                    QMessageBox.critical(None, "Erreur",
                                         f"L'âge ne saurait être supérieur à 100.\nCe n'est pas prévu par le code CIMA.\nEchec de l'enrégistrement.")
                    return

                if (nom, prenom) in [(ascendant.nom, ascendant.prenom) for ascendant in self.personne.enfants]:
                    return

                enfant = Enfant(nom=nom,
                                prenom=prenom,
                                age=age,
                                sexe=sexe,
                                poursuit_etudes=etudes,
                                handicap_majeur=handicap_majeur,
                                orphelin_double=orpehlin_double)

                self.personne.enfants.append(enfant)

                self.enfants_list.clear()
                for individu in self.personne.enfants:
                    self.enfants_list.addItem(
                        f"Nom : {individu.nom} \nPrénom : {individu.prenom} \nAge: {individu.age} ans \nSexe : {individu.sexe} \nPoursuit les études : {"Oui" if individu.poursuit_etudes else "Non"} \nHandicap majeur à vie : {"Oui" if individu.handicap_majeur else "Non"}")

        pass

    def valider_enregistrement(self):
        nom = self.profil_nom_le.text()
        prenom = self.profil_prenom_le.text()
        age = self.profil_age_le.text()
        profession = self.profil_profession_le.text()
        salaire = self.profil_salaire_le.texte()
        situation_matrimoniale = self.profil_matrimoniale_cb.currentText()
        sexe = self.profil_sexe_cb.currentText()
        pays_r = self.profil_pays_residence_cb.currentText()
        pays_s = self.profil_pays_sinistre_cb.currentText()

        if not nom or not prenom:
            QMessageBox.critical(None, "Erreur",
                                 f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
            return

        try:
            int(age)
        except:
            QMessageBox.critical(None, "Erreur",
                                 f"L'âge doit être une valeur numérique sans espace.\nEchec de l'enrégistrement.")
            return

        try:
            int(age) > 100
        except:
            QMessageBox.critical(None, "Erreur",
                                 f"L'âge ne saurait être supérieur à 100.\nCe n'est pas prévu par le code CIMA.\nEchec de l'enrégistrement.")
            return

        try:
            int(salaire)
        except:
            QMessageBox.critical(None, "Erreur",
                                 f"Le salaire doit être une valeur numérique sans espaces.\nEchec de l'enrégistrement.")
            return

        personne = Personne(
            nom=nom,
            prenom=prenom,
            age=int(age),
            profession=profession,
            salaire=int(salaire),
            situation_matrimoniale=situation_matrimoniale,
            pays_residence=pays_r,
            pays_sinistre=pays_s,
            sexe=sexe,
            age_limite=AGE_LIMITE,
            enfants=self.personne.enfants,
            conjoints=self.personne.conjoints,
            ascendants=self.personne.ascendants,
            collateraux=self.personne.collateraux
        )

        if self.modification:
            try:
                supprimer_et_reorganiser_ids(self.personne_index)
            except Exception as e:
                print(e)

        try:
            ajouter_personne_data_base(personne)
        except Exception as e:
            print(e)
        pass
    pass


main_window = QWidget()
main_window.setStyleSheet("""background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #B9D5F9,
        stop:0.6 #e8f2ff,
        stop:1 #d0e3ff
    );""")
main_layout = QHBoxLayout(main_window)
main_layout.addWidget(ModifierProfil(default_personne))
main_window.show()

if __name__ == '__main__':
    sys.exit(app.exec())