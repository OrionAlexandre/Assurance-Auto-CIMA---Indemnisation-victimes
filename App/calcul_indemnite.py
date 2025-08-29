from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QAction
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QPushButton, \
    QLineEdit, QComboBox, QCheckBox, QDialog, QGridLayout, QMessageBox, QMenu

from custom_widget import WidgetContainer, RepartitionWidget, CustomLabelName, ProfilLabel, ScrollableWidget, \
    CustomCalculusQWidget, ListVictime, ListConjoints, ListEnfants, ListAscendants, ListCollateraux, \
    CustomAyantsDroitsList
from api import data_contoller, format_nombre_fr, laod_default_personne_alive, error_logger
from database_manager import rechercher_personne_par_id, ajouter_personne_data_base, Personne

from algorithm.tables import SituationMatrimoniale, smig_pays_cima_2025, AGE_LIMITE, NiveauPrejudice
from algorithm.profils import Enfant, Conjoint, Ascendant, Collateral

from algorithm.alive import FraisDeTraitement, IncapaciteTemporaire, IncapacitePermanente, AssistanceTiercePersonne, \
    PretiumDoloris, PrejudiceEsthetique, PrejudicePerteDeGainsProfessinnelsFuturs, PrejudiceScolaire, \
    PrejudiceMoralConjoint


class NouveauProfil(QDialog):
    def __init__(self):

        if data_contoller.load_profil_alive:
            data_contoller.call_fonction(key="close_profil_alive")
        else:
            data_contoller.call_fonction(key="close_profil_dead")
        pass

        super().__init__()
        self.setStyleSheet("""background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #B9D5F9,
                stop:0.6 #e8f2ff,
                stop:1 #d0e3ff
            );
            border-radius: 8px;
            """)
        self.setModal(True)
        self.setFixedSize(900, 770)
        icon = QIcon(QPixmap("assets/078-android.png"))
        self.setWindowIcon(icon)

        self.__nouvelle_liste_enfants = []
        self.__nouvelle_liste_ascendants = []
        self.__nouvelle_liste_conjoints = []
        self.__nouvelle_liste_collateraux = []

        self.entries = self.Entries()
        self.buttons = self.ButtonGroup()

        main_layout = QHBoxLayout(self)

        # Widget de mise en arroère-plan.
        widget_back = QWidget()
        main_layout.addWidget(widget_back)


        widget_back.setStyleSheet("""
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
        """)

        principal_layout = QVBoxLayout(widget_back)

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(7)
        # self.__separator.setFixedWidth(1)
        self.__separator.setStyleSheet("background-color: #060270")
        principal_layout.addWidget(self.__separator)

        label_entete = QLabel("Création d'un nouveau profil")
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
        principal_layout.addWidget(label_entete)


        # La layout formulaire de la victime
        formulaire_layout = QGridLayout()
        principal_layout.addLayout(formulaire_layout)

        column = 0
        for label in [QLabel("Nom :"), QLabel("Prénom :"), QLabel("Age :")]:
            formulaire_layout.addWidget(label, 0, column)
            column += 1

        column = 0
        for entry in [self.entries.profil_nom_le, self.entries.profil_prenom_le, self.entries.profil_age_le]:
            formulaire_layout.addWidget(entry, 1, column)
            column += 1

        column = 0
        for label in [QLabel("Profession :"), QLabel("Salaire / Bourse mensuelle :"), QLabel("Situation matrimoniale :")]:
            formulaire_layout.addWidget(label, 2, column)
            column += 1

        column = 0
        for entry in [self.entries.profil_profession_le, self.entries.profil_salaire_le,
                      self.entries.profil_matrimoniale_le]:
            formulaire_layout.addWidget(entry, 3, column)
            column += 1

        column = 0
        for label in [QLabel("Pays de résidence :"), QLabel("Pays lieu du sinistre :")]:
            formulaire_layout.addWidget(label, 4, column)
            column += 1

        column = 0
        for entry in [self.entries.profil_pays_residence_le, self.entries.profil_pays_sinistre_le,
                      self.entries.profil_sexe_le]:
            formulaire_layout.addWidget(entry, 5, column)
            column += 1

        formulaire_layout.addWidget(self.buttons.ajouter_profil, 6, 2)

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(7)
        # self.__separator.setFixedWidth(1)
        self.__separator.setStyleSheet("background-color: #060270")
        principal_layout.addWidget(self.__separator)

        # Ajout d'un layout pour les profils des ayants droit de la victime.
        label_ayants_droit = QLabel("Les ayants droits")
        label_ayants_droit.setStyleSheet("""
            QLabel {
                color: #34495e;
                font-size: 16px;
                font-weight: 600;
                padding-bottom: 8px;
                border-bottom: 2px solid #3498db;  /* Ligne de séparation bleue */
                margin-bottom: 15px;
            }
        """)
        label_ayants_droit.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        principal_layout.addWidget(label_ayants_droit)

        ayants_droit_layout = QHBoxLayout()
        principal_layout.addLayout(ayants_droit_layout)

        #===========================================================
        enfants_layout = QGridLayout()
        label_enfant = QLabel("Enfant")
        label_enfant.setStyleSheet("font-weight: bold;")
        label_enfant.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        enfants_layout.addWidget(label_enfant, 0, 0, 1, 3)

        column = 0
        for label in [QLabel("Nom :"), QLabel("Prénom :")]:
            enfants_layout.addWidget(label, 1, column)
            column += 1

        column = 0
        for label in [self.entries.enfant_nom_le, self.entries.enfant_prenom_le]:
            enfants_layout.addWidget(label, 2, column)
            column += 1

        enfants_layout.addWidget(QLabel("Age :"), 3, 0)
        enfants_layout.addWidget(self.entries.enfant_age_le, 4, 0)

        enfants_layout.addWidget(QLabel("Sexe :"), 3, 1)
        enfants_layout.addWidget(self.entries.enfant_sexe_le, 4, 1)

        enfants_layout.addWidget(self.entries.enfant_etudes_le, 5, 0, 1, 2)
        enfants_layout.addWidget(self.entries.enfant_handicap_le, 6, 0, 1, 2)

        enfants_layout.addWidget(self.buttons.ajouter_enfant, 7, 0)
        enfants_layout.addWidget(self.buttons.lister_enfant, 7, 1)

        # ===========================================================
        conjoints_layout = QGridLayout()
        label_conjoint = QLabel("Conjoint")
        label_conjoint.setStyleSheet("font-weight: bold;")
        label_conjoint.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        conjoints_layout.addWidget(label_conjoint, 0, 0, 1, 2)

        row = 1
        for label in [QLabel("Nom :"), QLabel("Prénom :"), QLabel("Age:"), QLabel("Sexe :")]:
            conjoints_layout.addWidget(label, row, 0)
            row += 2

        row = 2
        for label in [self.entries.conjoint_nom_le, self.entries.conjoint_prenom_le,
                      self.entries.conjoint_age_le, self.entries.conjoint_sexe_le]:
            conjoints_layout.addWidget(label, row, 0, 1, 2)
            row += 2

        conjoints_layout.addWidget(self.buttons.ajouter_conjoint, 9, 0)
        conjoints_layout.addWidget(self.buttons.lister_conjoint, 9, 1)

        # ===========================================================
        ascendants_layout = QGridLayout()
        label_ascendant = QLabel("Ascendant")
        label_ascendant.setStyleSheet("font-weight: bold;")
        label_ascendant.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ascendants_layout.addWidget(label_ascendant, 0, 0, 1, 2)

        row = 1
        for label in [QLabel("Nom :"), QLabel("Prénom :"), QLabel("Age:"), QLabel("Sexe:")]:
            ascendants_layout.addWidget(label, row, 0)
            row += 2

        row = 2
        for label in [self.entries.ascendant_nom_le, self.entries.ascendant_prenom_le, self.entries.ascendant_age_le, self.entries.ascendant_sexe_le]:
            ascendants_layout.addWidget(label, row, 0, 1, 2)
            row += 2

        ascendants_layout.addWidget(self.buttons.ajouter_ascendant, 8, 0)
        ascendants_layout.addWidget(self.buttons.lister_ascendant, 8, 1)

        # ===========================================================
        collarteraux_layout = QGridLayout()
        label_collateral = QLabel("Collatéraux")
        label_collateral.setStyleSheet("font-weight: bold;")
        label_collateral.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        collarteraux_layout.addWidget(label_collateral, 0, 0, 1, 2)

        row = 1
        for label in [QLabel("Nom :"), QLabel("Prénom :"), QLabel("Age:")]:
            collarteraux_layout.addWidget(label, row, 0)
            row += 2

        row = 2
        for label in [self.entries.collateral_nom_le, self.entries.collateral_prenom_le, self.entries.collateral_age_le]:
            collarteraux_layout.addWidget(label, row, 0, 1, 2)
            row += 2

        collarteraux_layout.addWidget(self.buttons.ajouter_collateral, 7, 0)
        collarteraux_layout.addWidget(self.buttons.lister_collateral, 7, 1)

        # ===========================================================
        for layout in [enfants_layout, conjoints_layout, collarteraux_layout, ascendants_layout]:
            ayants_droit_layout.addLayout(layout)

            # Barre de séparation.
            self.__separator = QWidget()
            # self.__separator.setFixedHeight(30)
            self.__separator.setFixedWidth(1)
            self.__separator.setStyleSheet("background-color: #060270")
            ayants_droit_layout.addWidget(self.__separator)

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(7)
        # self.__separator.setFixedWidth(1)
        self.__separator.setStyleSheet("background-color: #060270")
        principal_layout.addWidget(self.__separator)

        # ===========================================================
        principal_layout.addWidget(self.buttons.ajouter_profil)
        self.buttons.ajouter_profil.setFixedSize(250, 30)
        self.buttons.ajouter_profil.setStyleSheet("""
                                        QPushButton {
                                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #2EA44F,       /* Vert GitHub vif */
                                                stop:1 #22863A);      /* Vert GitHub foncé */
                                            border: 1px solid #2EA44F;
                                            border-radius: 6px;
                                            color: white;             /* Texte blanc */
                                            font-weight: 600;         /* Gras moyen */
                                            margin-top: 7px;
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
        self.buttons.ajouter_profil.clicked.connect(self.enregistrer_personne)

        # Assignation des méthodes aux différents bouttons.
        self.buttons.ajouter_enfant.clicked.connect(self.ajouter_enfant)
        self.buttons.lister_enfant.clicked.connect(
            lambda : self.afficher_liste(list_to_show=self.__nouvelle_liste_enfants, enfant=True))

        self.buttons.ajouter_conjoint.clicked.connect(self.ajouter_conjoint)
        self.buttons.lister_conjoint.clicked.connect(
            lambda: self.afficher_liste(list_to_show=self.__nouvelle_liste_conjoints, conjoint=True))

        self.buttons.ajouter_ascendant.clicked.connect(self.ajouter_ascendant)
        self.buttons.lister_ascendant.clicked.connect(
            lambda: self.afficher_liste(list_to_show=self.__nouvelle_liste_ascendants))

        self.buttons.ajouter_collateral.clicked.connect(self.ajouter_collateral)
        self.buttons.lister_collateral.clicked.connect(
            lambda: self.afficher_liste(list_to_show=self.__nouvelle_liste_collateraux))

        self.entries.profil_nom_le.textChanged.connect(self.defining_nom_profil_and_others)
        self.entries.profil_sexe_le.currentTextChanged.connect(self.defining_sexe_conjoint)

    # ===========================================================
    def afficher_liste(self, list_to_show, enfant: bool = False, conjoint: bool = False):
        interface = QDialog()
        interface.setStyleSheet("""background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 #B9D5F9,
                        stop:0.6 #e8f2ff,
                        stop:1 #d0e3ff
                    );
                    border-radius: 8px;
                    """)
        interface.setModal(True)
        icon = QIcon(QPixmap("assets/078-android.png"))
        interface.setWindowIcon(icon)

        interface_layout = QVBoxLayout(interface)

        list_widget = CustomAyantsDroitsList()
        if enfant:
            for individu in list_to_show:
                list_widget.addItem(f"Nom : {individu.nom} \nPrénom : {individu.prenom} \nAge: {individu.age} ans \nSexe : {individu.sexe} \nPoursuit les études : {"Oui" if individu.poursuit_etudes else "Non"} \nHandicap majeur à vie : {"Oui" if individu.handicap_majeur else "Non"}")
                print(f"Nom :{individu.nom} - Prénom :{individu.prenom}")
        elif conjoint:
            for individu in list_to_show:
                list_widget.addItem(f"Nom : {individu.nom} \nPrénom : {individu.prenom} \nAge: {individu.age} ans \nSexe : {individu.sexe}")
                print(f"Nom :{individu.nom} - Prénom :{individu.prenom}")
        else:
            for individu in list_to_show:
                list_widget.addItem(f"Nom : {individu.nom} \nPrénom : {individu.prenom} \nAge: {individu.age} ans")
                print(f"Nom :{individu.nom} - Prénom :{individu.prenom}")

        interface_layout.addWidget(list_widget)
        interface.show()
        interface.exec()
        pass

    def ajouter_enfant(self):
        from database_manager import Enfant

        nom_enfant = self.entries.enfant_nom_le.text()
        prenom_enfant = self.entries.enfant_prenom_le.text()

        if not nom_enfant or not prenom_enfant:
            QMessageBox.critical(None, "Erreur", f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
            return

        try:
            age_enfant = int(self.entries.enfant_age_le.text())
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Une valeur d'âge erronée :\n{str(e)}.\nEchec de l'enrégistrement.")
            return

        sexe_enfant = self.entries.enfant_sexe_le.currentText()
        handicap_enfant = self.entries.enfant_handicap_le.isChecked()
        etude_enfant = self.entries.enfant_etudes_le.isChecked()

         # Création du profil de l'enfant.
        enfant = Enfant(nom=nom_enfant,
                        prenom=prenom_enfant,
                        age=age_enfant,
                        sexe=sexe_enfant,
                        poursuit_etudes=etude_enfant,
                        handicap_majeur=handicap_enfant)
        self.__nouvelle_liste_enfants.append(
            enfant) if (enfant.nom, enfant.prenom) not in [(enfant.nom, enfant.prenom) for enfant in self.__nouvelle_liste_enfants] else None
        pass

    def ajouter_conjoint(self):
        from database_manager import Conjoint

        nom_conjoint = self.entries.conjoint_nom_le.text()
        prenom_conjoint = self.entries.conjoint_prenom_le.text()

        if not nom_conjoint or not prenom_conjoint:
            QMessageBox.critical(None, "Erreur", f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
            return

        try:
            age_conjoint = int(self.entries.conjoint_age_le.text())
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Une valeur d'âge erronée :\n{str(e)}.\nEchec de l'enrégistrement.")
            return

        sexe_conjoint = self.entries.conjoint_sexe_le.currentText()

        conjoint = Conjoint(nom=nom_conjoint,
                            prenom=prenom_conjoint,
                            age=age_conjoint,
                            sexe=sexe_conjoint)

        self.__nouvelle_liste_conjoints.append(
            conjoint) if (conjoint.nom, conjoint.prenom) not in [(conjoint.nom, conjoint.prenom) for conjoint in self.__nouvelle_liste_conjoints] else None
        pass

    def ajouter_ascendant(self):
        from database_manager import Ascendant

        nom_ascendant = self.entries.ascendant_nom_le.text()
        prenom_ascendant = self.entries.ascendant_prenom_le.text()

        if not nom_ascendant or not prenom_ascendant:
            QMessageBox.critical(None, "Erreur", f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
            return

        try:
            age_ascendant = int(self.entries.ascendant_age_le.text())
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Une erreur s'est produite :\n{str(e)}.\nEchec de l'enrégistrement.")
            return

        sexe_ascendant = self.entries.ascendant_sexe_le.currentText()

        ascendant = Ascendant(nom=nom_ascendant,
                            prenom=prenom_ascendant,
                            age=age_ascendant,
                            sexe=sexe_ascendant)

        self.__nouvelle_liste_ascendants.append(
            ascendant) if (ascendant.nom, ascendant.prenom) not in [(ascendant.nom, ascendant.prenom) for ascendant in self.__nouvelle_liste_ascendants] else None
        pass

    def ajouter_collateral(self):
        from database_manager import Collateral

        nom_collateral = self.entries.collateral_nom_le.text()
        prenom_collateral = self.entries.collateral_prenom_le.text()

        if not nom_collateral or not prenom_collateral:
            QMessageBox.critical(None, "Erreur", f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
            return

        try:
            age_collateral = int(self.entries.collateral_age_le.text())
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Une valeur d'âge erronée :\n{str(e)}.\nEchec de l'enrégistrement.")
            return

        collateral = Collateral(nom=nom_collateral,
                             prenom=prenom_collateral,
                             age=age_collateral)

        self.__nouvelle_liste_collateraux.append(
            collateral) if (collateral.nom, collateral.prenom) not in [(collateral.nom, collateral.prenom) for collateral in self.__nouvelle_liste_collateraux] else None
        pass

    def enregistrer_personne(self):
        from database_manager import Personne

        nom_personne = self.entries.profil_nom_le.text()
        prenom_personne = self.entries.profil_prenom_le.text()

        if not nom_personne or not prenom_personne:
            QMessageBox.critical(None, "Erreur", f"Le nom et le prénom sont exigés.\nEchec de l'enrégistrement.")
            return

        try:
            age_personne = int(self.entries.profil_age_le.text())
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Une valeur d'âge erronée :\n{str(e)}.\n\nEchec de l'enrégistrement.")
            return

        profession_personne = self.entries.profil_profession_le.text()

        try:
            salaire_personne = int(self.entries.profil_salaire_le.text())
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Une valeur salaire erronée :\n{str(e)}.\n\nEchec de l'enrégistrement.")
            return

        situation_matrimoniale = self.entries.profil_matrimoniale_le.currentText()
        pays_residence = self.entries.profil_pays_residence_le.currentText()
        pays_sinistre = self.entries.profil_pays_sinistre_le.currentText()
        sexe_personne = self.entries.profil_sexe_le.currentText()

        # Création du profil de la victime.
        personne = Personne(nom=nom_personne,
                            prenom=prenom_personne,
                            age=age_personne,
                            sexe=sexe_personne,
                            age_limite=AGE_LIMITE,
                            profession=profession_personne,
                            salaire=salaire_personne,
                            situation_matrimoniale=situation_matrimoniale,
                            conjoints=self.__nouvelle_liste_conjoints,
                            enfants=self.__nouvelle_liste_enfants,
                            ascendants=self.__nouvelle_liste_ascendants,
                            collateraux=self.__nouvelle_liste_collateraux,
                            pays_residence=pays_residence,
                            pays_sinistre=pays_sinistre)

        # Insertion de la personne dans la base de données.
        ajouter_personne_data_base(personne)

        if data_contoller.load_profil_alive:
            data_contoller.call_fonction(key="load_profil_alive")
        else:
            data_contoller.call_fonction(key="load_profil_dead")

        self.close() # On ferme la fenêtre de création d'un nouveau profil.
        pass

    def defining_nom_profil_and_others(self, text):
        self.entries.enfant_nom_le.setText(text)
        self.entries.conjoint_nom_le.setText(text)
        self.entries.ascendant_nom_le.setText(text)
        self.entries.collateral_nom_le.setText(text)
        pass

    def defining_sexe_conjoint(self, sexe):
        if sexe == "M":
            self.entries.conjoint_sexe_le.setCurrentText("F")
        else:
            self.entries.conjoint_sexe_le.setCurrentText("M")

    class Entries:
        def __init__(self):
            from algorithm.tables import list_pays_cima
            # ===========================================================
            self.profil_nom_le = QLineEdit()
            self.profil_prenom_le = QLineEdit()
            self.profil_age_le = QLineEdit()

            self.profil_profession_le = QLineEdit()
            self.profil_salaire_le = QLineEdit()
            self.profil_matrimoniale_le = QComboBox()
            self.profil_matrimoniale_le.addItems([SituationMatrimoniale.CELIBATAIRE,
                                                  SituationMatrimoniale.MARIE_E,
                                                  SituationMatrimoniale.DIVORCE,
                                                  SituationMatrimoniale.VEUF_VE])
            self.profil_sexe_le = QComboBox()
            self.profil_sexe_le.addItems(["M", "F"])

            self.profil_pays_residence_le = QComboBox()
            self.profil_pays_sinistre_le = QComboBox()

            for cbbx in [self.profil_pays_residence_le, self.profil_pays_sinistre_le]:
                cbbx.addItems(list_pays_cima)

            # ===========================================================
            self.enfant_nom_le = QLineEdit()
            self.enfant_prenom_le = QLineEdit()
            self.enfant_age_le = QLineEdit()
            self.enfant_sexe_le = QComboBox()
            self.enfant_sexe_le.addItems(["M", "F"])
            self.enfant_etudes_le = QCheckBox("L'enfant continue-t-il ses études ?")
            self.enfant_handicap_le = QCheckBox("L'enfant justifie-t-il d'un handicap sévère ?")

            # ===========================================================
            self.conjoint_nom_le = QLineEdit()
            self.conjoint_prenom_le = QLineEdit()
            self.conjoint_age_le = QLineEdit()
            self.conjoint_sexe_le = QComboBox()
            self.conjoint_sexe_le.addItems(["M", "F"])

            # ===========================================================
            self.collateral_nom_le = QLineEdit()
            self.collateral_prenom_le = QLineEdit()
            self.collateral_age_le = QLineEdit()

            # ===========================================================
            self.ascendant_nom_le = QLineEdit()
            self.ascendant_prenom_le = QLineEdit()
            self.ascendant_age_le = QLineEdit()
            self.ascendant_sexe_le = QComboBox()
            self.ascendant_sexe_le.addItems(["M", "F"])

    class ButtonGroup:
        def __init__(self):
            button_style = """
                    QPushButton {
                                    background: qlineargradient(
                                        x1: 0, y1: 0,
                                        x2: 1, y2: 1,  /* Diagonale ↘ */
                                        stop: 0 #63c966,     /* Vert vif en haut à gauche */
                                        stop: 0.5 #57b45b,   /* Vert moyen au centre */
                                        stop: 1 #4fa254      /* Vert plus foncé en bas à droite */
                                    );
                                    border: none;
                                    border-radius: 3px;
                                    margin-right: 7px;
                                    padding-bottom: 3px;
                                    padding-left: 10px;
                                    color: #ffffff;
                                    font-weight: 500;
                                    font-size: 12pt;
                                    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
                                }

                                QPushButton:hover {
                                    background: qlineargradient(
                                        x1: 0, y1: 0,
                                        x2: 1, y2: 1,
                                        stop: 0 #55b45c,
                                        stop: 1 #419a47
                                    );
                                    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
                                }

                                QPushButton:pressed {
                                    background: qlineargradient(
                                        x1: 0, y1: 0,
                                        x2: 1, y2: 1,
                                        stop: 0 #3f8f3f,
                                        stop: 1 #347a39
                                    );
                                    color: #d5e9d1;
                                    box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.3);
                                }
                    """
            red_button_style = """
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff5252,    /* Rouge vif */
                    stop:0.5 #ff3d3d,  /* Rouge intense */
                    stop:1 #ff1744     /* Rouge profond */
                );
                border: none;
                border-radius: 3px;
                padding-bottom: 3px;
                padding-left: 10px;
                color: white;
                font-weight: 500;
                font-size: 12pt;
                font-family: 'Segoe UI', sans-serif;
                margin: 2px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }

            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff6b68,
                    stop:1 #ff2d4a
                );
                box-shadow: 0 2px 5px rgba(0,0,0,0.16);
                transform: translateY(-1px);
            }

            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e53935,
                    stop:1 #c62828
                );
                color: #ffebee;
                box-shadow: inset 0 1px 2px rgba(0,0,0,0.2), 
                            0 1px 1px rgba(0,0,0,0.1);
                transform: translateY(0);
            }

            QPushButton:disabled {
                background: #ef9a9a;
                color: #ffebee;
                box-shadow: none;
            }
            """

            self.ajouter_profil = QPushButton("Ajouter ➕")
            self.ajouter_profil.setStyleSheet(button_style)

            self.ajouter_enfant = QPushButton("Ajouter ➕")
            self.ajouter_enfant.setStyleSheet(button_style)
            self.lister_enfant = QPushButton("Liste 🗒️")
            self.lister_enfant.setStyleSheet(red_button_style)

            self.ajouter_conjoint = QPushButton("Ajouter ➕")
            self.ajouter_conjoint.setStyleSheet(button_style)
            self.lister_conjoint = QPushButton("Liste 🗒️")
            self.lister_conjoint.setStyleSheet(red_button_style)

            self.ajouter_collateral = QPushButton("Ajouter ➕")
            self.ajouter_collateral.setStyleSheet(button_style)
            self.lister_collateral = QPushButton("Liste 🗒️")
            self.lister_collateral.setStyleSheet(red_button_style)

            self.ajouter_ascendant = QPushButton("Ajouter ➕")
            self.ajouter_ascendant.setStyleSheet(button_style)
            self.lister_ascendant = QPushButton("Liste 🗒️")
            self.lister_ascendant.setStyleSheet(red_button_style)
        pass

    pass


class ListProfilsAlive(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 #B9D5F9,
                        stop:0.6 #e8f2ff,
                        stop:1 #d0e3ff
                    );
                    border-radius: 8px;
                    """)
        self.setModal(True)

        self.main_layout = QVBoxLayout(self)

        self.__list_vitimes = ListVictime()
        self.__list_enfants = ListEnfants(self.__list_vitimes.personne)
        self.__list_conjoints = ListConjoints(self.__list_vitimes.personne)
        self.__list_ascendants = ListAscendants(self.__list_vitimes.personne)
        self.__list_collateraux = ListCollateraux(self.__list_vitimes.personne)

        # self.__list_vitimes.itemDoubleClicked.connect(self.__item_double_clicked) # Le double click
        # servira à charger les données.
        self.__list_vitimes.itemPressed.connect(self.__item_pressed_clicked)
        self.__list_vitimes.itemDoubleClicked.connect(self.__item_double_clicked)
        self.__list_vitimes.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu) # Pour le click contextuel.

        # Connecter le signal de menu contextuel
        self.__list_vitimes.customContextMenuRequested.connect(self.__afficher_menu_contextuel)

        label_list_personnes = QLabel("Listes des victimes : Double-cliquer pour sélectionner.")
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

        # ====================================================================================
        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)

        # Le boutton de rajout des profils de victimes.
        self.nouveau_profil_btn = QPushButton("👤Nouveau profil")
        self.nouveau_profil_btn.setFixedSize(250, 30)
        self.nouveau_profil_btn.setStyleSheet("""
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
        self.nouveau_profil_btn.clicked.connect(self.nouveau_profil)
        button_layout.addWidget(self.nouveau_profil_btn)

        # Le boutton de rajout des profils de victimes.
        self.charger_profil_btn = QPushButton("📜Charger le profil")
        self.charger_profil_btn.setFixedSize(250, 30)
        self.charger_profil_btn.setStyleSheet("""
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
        self.charger_profil_btn.clicked.connect(self.__charger_profil)
        button_layout.addWidget(self.charger_profil_btn)

        # Le boutton de rajout des profils de victimes.
        self.supprimer_profil_btn = QPushButton("🚮Supprimer")
        self.supprimer_profil_btn.setFixedSize(250, 30)
        self.supprimer_profil_btn.setStyleSheet("""
                                        QPushButton {
                                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #cb2431,       /* Rouge GitHub vif */
                                                stop:1 #a41825);      /* Rouge GitHub foncé */
                                            border: 1px solid #cb2431;
                                            border-radius: 6px;
                                            color: white;             /* Texte blanc */
                                            font-weight: 600;         /* Gras moyen */
                                            padding: 5px;
                                            font-size: 12px;
                                        }
                                        
                                        QPushButton:hover {
                                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #d73a49,       /* Rouge GitHub clair (survol) */
                                                stop:1 #bc2c38);      /* Rouge GitHub moyen */
                                            border-color: #d73a49;
                                        }
                                        
                                        QPushButton:pressed {
                                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #a41825,       /* Rouge foncé */
                                                stop:1 #8b141f);      /* Rouge très foncé */
                                        }
                                    """)
        self.supprimer_profil_btn.clicked.connect(self.__supprimer_profil)
        button_layout.addWidget(self.supprimer_profil_btn)


    def nouveau_profil(self):
        nouveau_profil = NouveauProfil()
        nouveau_profil.show()
        nouveau_profil.exec()
    # ====================================================================================

    def __item_pressed_clicked(self, item):
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

    def __item_double_clicked(self, item):
        from api import save_default_personne_alive

        # Récupération de l'index (avec vérification)
        selected_row = self.__list_vitimes.row(item)
        if selected_row < 0:
            print("Aucun élément sélectionné")
            return

        personne = rechercher_personne_par_id(selected_row + 1)

        save_default_personne_alive(personne)

        data_contoller.call_fonction("load_profil_alive")

        # Fermeture de la QDialog.
        self.close()
        pass

    def __charger_profil(self):
        from api import save_default_personne_alive

        selected_row = self.__list_vitimes.currentRow()

        if selected_row <= 0:
            print("Aucun élément sélectionné")
            QMessageBox.critical(None, "Erreur", "Choisissez une victime.")
            return

        personne = rechercher_personne_par_id(selected_row + 1)

        save_default_personne_alive(personne)

        data_contoller.call_fonction("load_profil_alive")

        # Fermeture de la QDialog.
        self.close()
        pass

    def __supprimer_profil(self):
        from database_manager import supprimer_et_reorganiser_ids

        selected_row = self.__list_vitimes.currentRow()

        if selected_row < 0:
            print("Aucun élément sélectionné")
            QMessageBox.critical(None, "Erreur", "Choisissez une victime.")
            return

        self.__list_vitimes.takeItem(selected_row)

        self.__list_enfants.clear()
        self.__list_conjoints.clear()
        self.__list_ascendants.clear()
        self.__list_collateraux.clear()

        supprimer_et_reorganiser_ids(selected_row + 1)
        pass

    def __afficher_menu_contextuel(self, position):
        index = self.__list_vitimes.indexAt(position)

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

        action_modifier = QAction("✏️ Modifier", self)
        menu.addAction(action_modifier)

        menu.exec(self.__list_vitimes.mapToGlobal(position))
        pass


class ListProfilsDead(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 #B9D5F9,
                        stop:0.6 #e8f2ff,
                        stop:1 #d0e3ff
                    );
                    border-radius: 8px;
                    """)
        self.setModal(True)

        self.main_layout = QVBoxLayout(self)

        self.__list_vitimes = ListVictime()
        self.__list_enfants = ListEnfants(self.__list_vitimes.personne)
        self.__list_conjoints = ListConjoints(self.__list_vitimes.personne)
        self.__list_ascendants = ListAscendants(self.__list_vitimes.personne)
        self.__list_collateraux = ListCollateraux(self.__list_vitimes.personne)

        # self.__list_vitimes.itemDoubleClicked.connect(self.__item_double_clicked) # Le double click
        # servira à charger les données.
        self.__list_vitimes.itemPressed.connect(self.__item_pressed_clicked)
        self.__list_vitimes.itemDoubleClicked.connect(self.__item_double_clicked)
        self.__list_vitimes.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # Pour le click contextuel.

        # Connecter le signal de menu contextuel
        self.__list_vitimes.customContextMenuRequested.connect(self.__afficher_menu_contextuel)

        label_list_personnes = QLabel("Listes des victimes : Double-cliquer pour sélectionner.")
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

        # ====================================================================================
        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)

        # Le boutton de rajout des profils de victimes.
        self.nouveau_profil_btn = QPushButton("👤Nouveau profil")
        self.nouveau_profil_btn.setFixedSize(250, 30)
        self.nouveau_profil_btn.setStyleSheet("""
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
        self.nouveau_profil_btn.clicked.connect(self.nouveau_profil)
        button_layout.addWidget(self.nouveau_profil_btn)

        # Le boutton de rajout des profils de victimes.
        self.charger_profil_btn = QPushButton("📜Charger le profil")
        self.charger_profil_btn.setFixedSize(250, 30)
        self.charger_profil_btn.setStyleSheet("""
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
        self.charger_profil_btn.clicked.connect(self.__charger_profil)
        button_layout.addWidget(self.charger_profil_btn)

        # Le boutton de rajout des profils de victimes.
        self.supprimer_profil_btn = QPushButton("🚮Supprimer")
        self.supprimer_profil_btn.setFixedSize(250, 30)
        self.supprimer_profil_btn.setStyleSheet("""
                                                QPushButton {
                                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 #cb2431,       /* Rouge GitHub vif */
                                                        stop:1 #a41825);      /* Rouge GitHub foncé */
                                                    border: 1px solid #cb2431;
                                                    border-radius: 6px;
                                                    color: white;             /* Texte blanc */
                                                    font-weight: 600;         /* Gras moyen */
                                                    padding: 5px;
                                                    font-size: 12px;
                                                }

                                                QPushButton:hover {
                                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 #d73a49,       /* Rouge GitHub clair (survol) */
                                                        stop:1 #bc2c38);      /* Rouge GitHub moyen */
                                                    border-color: #d73a49;
                                                }

                                                QPushButton:pressed {
                                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 #a41825,       /* Rouge foncé */
                                                        stop:1 #8b141f);      /* Rouge très foncé */
                                                }
                                            """)
        self.supprimer_profil_btn.clicked.connect(self.__supprimer_profil)
        button_layout.addWidget(self.supprimer_profil_btn)

    def nouveau_profil(self):
        nouveau_profil = NouveauProfil()
        nouveau_profil.show()
        nouveau_profil.exec()
    #====================================================================================

    def __item_pressed_clicked(self, item):
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

    def __item_double_clicked(self, item):
        from api import save_default_personne_dead

        # Récupération de l'index (avec vérification)
        selected_row = self.__list_vitimes.row(item)
        if selected_row < 0:
            print("Aucun élément sélectionné")
            return

        personne = rechercher_personne_par_id(selected_row + 1)

        save_default_personne_dead(personne)

        data_contoller.call_fonction("load_profil_dead")
        data_contoller.call_fonction("recreate_repartition")
        # Fermeture de la QDialog.
        self.close()
        pass

    def __charger_profil(self):
        from api import save_default_personne_dead

        selected_row = self.__list_vitimes.currentRow()

        if selected_row <= 0:
            print("Aucun élément sélectionné")
            QMessageBox.critical(None, "Erreur", "Choisissez une victime.")
            return

        personne = rechercher_personne_par_id(selected_row + 1)

        save_default_personne_dead(personne)

        data_contoller.call_fonction("load_profil_dead")
        data_contoller.call_fonction("recreate_repartition")

        # Fermeture de la QDialog.
        self.close()
        pass

    def __supprimer_profil(self):
        from database_manager import supprimer_et_reorganiser_ids

        selected_row = self.__list_vitimes.currentRow()

        if selected_row < 0:
            print("Aucun élément sélectionné")
            QMessageBox.critical(None, "Erreur", "Choisissez une victime.")
            return

        self.__list_vitimes.takeItem(selected_row)

        self.__list_enfants.clear()
        self.__list_conjoints.clear()
        self.__list_ascendants.clear()
        self.__list_collateraux.clear()

        supprimer_et_reorganiser_ids(selected_row + 1)
        pass

    def __afficher_menu_contextuel(self, position):
        index = self.__list_vitimes.indexAt(position)

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

        action_modifier = QAction("✏️ Modifier", self)
        menu.addAction(action_modifier)

        menu.exec(self.__list_vitimes.mapToGlobal(position))
        pass


class ProfilAlive(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1200, 300)
        icon = QIcon(QPixmap("assets/030-list-1.png"))
        self.setWindowIcon(icon)
        self.setWindowTitle("Sélection du profil de la victime")
        self.setStyleSheet("""
                    QWidget {
                        background: qlineargradient(
                        x1: 0, y1: 0,
                        x2: 1, y2: 1,  /* Diagonale ↘ */
                        stop: 0 #252475,
                        stop: 0.7 #4B49F0,
                        stop: 1 #3736B0
                        );
                        border-radius: 8px;
                    }
                    QLabel {
                        background: rgba(0, 0, 0, 0);
                    }
                    QLabel#label_intitule {
                        font-size: 15pt;
                        font-weight: bold;
                    }
                    QLabel#profile_picture {
                        background-color: qlineargradient(
                        x1: 0, y1: 0,
                        x2: 1, y2: 1,  /* Diagonale ↘ */
                        stop: 0 #252475,
                        stop: 0.7 #4B49F0,
                        stop: 1 #3736B0);
                        margin-right: 7px;
                    }
                    QPushButton {
                        background: qlineargradient(
                            x1: 0, y1: 0,
                            x2: 1, y2: 1,  /* Diagonale ↘ */
                            stop: 0 #63c966,     /* Vert vif en haut à gauche */
                            stop: 0.5 #57b45b,   /* Vert moyen au centre */
                            stop: 1 #4fa254      /* Vert plus foncé en bas à droite */
                        );
                        border: none;
                        border-radius: 7px;
                        margin-right: 7px;
                        padding-left: 60px;
                        color: #ffffff;
                        font-weight: 500;
                        font-size: 12pt;
                        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
                    }

                    QPushButton:hover {
                        background: qlineargradient(
                            x1: 0, y1: 0,
                            x2: 1, y2: 1,
                            stop: 0 #55b45c,
                            stop: 1 #419a47
                        );
                        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
                    }

                    QPushButton:pressed {
                        background: qlineargradient(
                            x1: 0, y1: 0,
                            x2: 1, y2: 1,
                            stop: 0 #3f8f3f,
                            stop: 1 #347a39
                        );
                        color: #d5e9d1;
                        box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.3);
                    }

                """)

        self.button_group = self.ButtonGroup()
        self.profil_informations = self.ProfilInformations()

        self.main_layout = QHBoxLayout(self)
        self.__profile_widget = QWidget()
        self.main_layout.addWidget(self.__profile_widget)

        self.__profile_widget_layout = QHBoxLayout(self.__profile_widget)

        self.__profil_widget = QWidget()
        self.__first_widget = QWidget()
        self.__second_widget = QWidget()
        self.__third_widget = QWidget()

        for widget in [self.__profil_widget, self.__first_widget, self.__second_widget, self.__third_widget]:
            self.__profile_widget_layout.addWidget(widget)

        self.__profil_layout = QVBoxLayout(self.__profil_widget) # Photo de profil, boutton de chargement.
        self.__frist_layout = QVBoxLayout(self.__first_widget)  # Nom, prénom, âge.
        self.__second_layout = QVBoxLayout(self.__second_widget)  # Profession, salaire, situation matrimoniale.
        self.__thrid_layout = QVBoxLayout(self.__third_widget)  # Pays de résidence/smig, Pays sinistre/smig, smig retenu.

        #==============================================================================================================
        # Photo de profil, boutton de chargement.
        # ==============================================================================================================
        self.profile_picture = QLabel()
        self._profile = QPixmap("assets/039-user.png").scaled(150, 150)
        self.profile_picture.setPixmap(self._profile)
        # self.profile_picture.setObjectName("profile_picture")
        self.profile_picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__profil_layout.addWidget(self.profile_picture)
        self.__profil_layout.addWidget(self.button_group.modifier_profile)

        # ==============================================================================================================
        # Nom, prénom, âge.
        # ==============================================================================================================
        label_nom = CustomLabelName("Nom :")
        self.__frist_layout.addWidget(label_nom)
        self.__frist_layout.addWidget(self.profil_informations.nom)

        label_prenom = CustomLabelName("Prenom :")
        self.__frist_layout.addWidget(label_prenom)
        self.__frist_layout.addWidget(self.profil_informations.prenom)

        label_age = CustomLabelName("Age :")
        self.__frist_layout.addWidget(label_age)
        self.__frist_layout.addWidget(self.profil_informations.age)

        # ==============================================================================================================
        # Profession, salaire, situation matrimoniale.
        # ==============================================================================================================
        label_profession = CustomLabelName("Profession :")
        self.__second_layout.addWidget(label_profession)
        self.__second_layout.addWidget(self.profil_informations.profession)

        label_salaire = CustomLabelName("Salaire / Bourse mensuelle :")
        self.__second_layout.addWidget(label_salaire)
        self.__second_layout.addWidget(self.profil_informations.salaire)

        label_matrimoniale = CustomLabelName("Situation matrimoniale :")
        self.__second_layout.addWidget(label_matrimoniale)
        self.__second_layout.addWidget(self.profil_informations.matrimoniale)

        # ==============================================================================================================
        # Pays de résidence/smig, Pays sinistre/smig, smig retenu.
        # ==============================================================================================================
        label_pays_r = CustomLabelName("Pays de résidence/SMIG :")
        self.__thrid_layout.addWidget(label_pays_r)
        self.__thrid_layout.addWidget(self.profil_informations.pays_residence)

        label_pays_s = CustomLabelName("Pays lieu du sinistre/SMIG :")
        self.__thrid_layout.addWidget(label_pays_s)
        self.__thrid_layout.addWidget(self.profil_informations.pays_sinistre)

        label_smig = CustomLabelName("SMIG Retenu :")
        self.__thrid_layout.addWidget(label_smig)
        self.__thrid_layout.addWidget(self.profil_informations.smig_retenu)

        # Chargement du profil de la victime.
        self.load_profil_alive()

        # Enregistrement de la méthode d'appel.
        data_contoller.add_callable_function(key="load_profil_alive", func=self.load_profil_alive)
        data_contoller.add_callable_function(key="close_profil_alive", func=self.close())

    def load_profil_alive(self):
        from api import laod_default_personne_alive
        print("--------------------------------------------------------------")
        default_personne = laod_default_personne_alive()
        print("Chargement du profil... : Personne :", default_personne.nom)
        try:
            # Récupérer depuis le data_controller
            self.profil_informations.nom.setText(default_personne.nom)
            self.profil_informations.prenom.setText(default_personne.prenom)
            self.profil_informations.age.setText(f"{default_personne.age} ans")

            self.profil_informations.profession.setText(default_personne.profession)
            self.profil_informations.salaire.setText(f"{format_nombre_fr(default_personne.salaire)} F CFA")
            self.profil_informations.matrimoniale.setText(default_personne.situation_matrimoniale)

            # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
            smig_residence = smig_pays_cima_2025.get(default_personne.pays_residence)
            smig_sinistre = smig_pays_cima_2025.get(default_personne.pays_sinistre)

            # Définition du smig à retenir pour le calcul du plafond et des indemnités.
            smig = max(smig_residence,
                       smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

            self.profil_informations.pays_residence.setText(
                f"{default_personne.pays_residence} / {format_nombre_fr(smig_residence)} F CFA")
            self.profil_informations.pays_sinistre.setText(
                f"{default_personne.pays_sinistre} / {format_nombre_fr(smig_sinistre)} F CFA")
            self.profil_informations.smig_retenu.setText(f"{format_nombre_fr(smig)} F CFA")

            print("Fin du chargement du profil... Personne :", default_personne.nom)
            print("--------------------------------------------------------------")
        except Exception as e:
            error_logger.log_error(message=e, exception=e)
            print(e)

        # Afin de pouvoir restaurer la dernière fenêtre.
        data_contoller.load_profil_alive = True
        pass

        # ==============================================================================================================
        # ==============================================================================================================

    # Cette classe sera le domaine qui contiendra tous les bouttons de ce widget.
    class ButtonGroup:
        def __init__(self):
            self.modifier_profile = QPushButton("Charger profil 🖊️")
            self.modifier_profile.setFixedSize(250, 30)
            self.modifier_profile.setStyleSheet("""
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

            self.modifier_profile.clicked.connect(self.charger_profil)

        def charger_profil(self):
            charger_profil = ListProfilsAlive()
            charger_profil.show()
            charger_profil.exec()

        pass

    class ProfilInformations:
        def __init__(self):
            self.nom =ProfilLabel("-")
            self.prenom = ProfilLabel("-")
            self.age = ProfilLabel("-")

            self.profession = ProfilLabel("-")
            self.salaire = ProfilLabel("-")
            self.matrimoniale = ProfilLabel("-")

            self.pays_residence = ProfilLabel("-")
            self.pays_sinistre = ProfilLabel("-")
            self.smig_retenu = ProfilLabel("-")
    pass


class ProfilDead(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1200, 300)
        icon = QIcon(QPixmap("assets/030-list-1.png"))
        self.setWindowIcon(icon)
        self.setWindowTitle("Sélection du profil de la victime")
        self.setStyleSheet("""
                    QWidget {
                        background: qlineargradient(
                        x1: 0, y1: 0,
                        x2: 1, y2: 1,  /* Diagonale ↘ */
                        stop: 0 #252475,
                        stop: 0.7 #4B49F0,
                        stop: 1 #3736B0
                        );
                        border-radius: 8px;
                    }
                    QLabel {
                        background: rgba(0, 0, 0, 0);
                    }
                    QLabel#label_intitule {
                        font-size: 15pt;
                        font-weight: bold;
                    }
                    QLabel#profile_picture {
                        background-color: qlineargradient(
                        x1: 0, y1: 0,
                        x2: 1, y2: 1,  /* Diagonale ↘ */
                        stop: 0 #252475,
                        stop: 0.7 #4B49F0,
                        stop: 1 #3736B0);
                        margin-right: 7px;
                    }
                    QPushButton {
                        background: qlineargradient(
                            x1: 0, y1: 0,
                            x2: 1, y2: 1,  /* Diagonale ↘ */
                            stop: 0 #63c966,     /* Vert vif en haut à gauche */
                            stop: 0.5 #57b45b,   /* Vert moyen au centre */
                            stop: 1 #4fa254      /* Vert plus foncé en bas à droite */
                        );
                        border: none;
                        border-radius: 7px;
                        margin-right: 7px;
                        padding-left: 60px;
                        color: #ffffff;
                        font-weight: 500;
                        font-size: 12pt;
                        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
                    }

                    QPushButton:hover {
                        background: qlineargradient(
                            x1: 0, y1: 0,
                            x2: 1, y2: 1,
                            stop: 0 #55b45c,
                            stop: 1 #419a47
                        );
                        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
                    }

                    QPushButton:pressed {
                        background: qlineargradient(
                            x1: 0, y1: 0,
                            x2: 1, y2: 1,
                            stop: 0 #3f8f3f,
                            stop: 1 #347a39
                        );
                        color: #d5e9d1;
                        box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.3);
                    }

                """)

        self.button_group = self.ButtonGroup()
        self.profil_informations = self.ProfilInformations()

        self.main_layout = QHBoxLayout(self)
        self.__profile_widget = QWidget()
        self.main_layout.addWidget(self.__profile_widget)

        self.__profile_widget_layout = QHBoxLayout(self.__profile_widget)

        self.__profil_widget = QWidget()
        self.__first_widget = QWidget()
        self.__second_widget = QWidget()
        self.__third_widget = QWidget()

        for widget in [self.__profil_widget, self.__first_widget, self.__second_widget, self.__third_widget]:
            self.__profile_widget_layout.addWidget(widget)

        self.__profil_layout = QVBoxLayout(self.__profil_widget)  # Photo de profil, boutton de chargement.
        self.__frist_layout = QVBoxLayout(self.__first_widget)  # Nom, prénom, âge.
        self.__second_layout = QVBoxLayout(self.__second_widget)  # Profession, salaire, situation matrimoniale.
        self.__thrid_layout = QVBoxLayout(
            self.__third_widget)  # Pays de résidence/smig, Pays sinistre/smig, smig retenu.

        # ==============================================================================================================
        # Photo de profil, boutton de chargement.
        # ==============================================================================================================
        self.profile_picture = QLabel()
        self._profile = QPixmap("assets/039-user.png").scaled(150, 150)
        self.profile_picture.setPixmap(self._profile)
        # self.profile_picture.setObjectName("profile_picture")
        self.profile_picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__profil_layout.addWidget(self.profile_picture)
        self.__profil_layout.addWidget(self.button_group.modifier_profile)

        # ==============================================================================================================
        # Nom, prénom, âge.
        # ==============================================================================================================
        label_nom = CustomLabelName("Nom :")
        self.__frist_layout.addWidget(label_nom)
        self.__frist_layout.addWidget(self.profil_informations.nom)

        label_prenom = CustomLabelName("Prenom :")
        self.__frist_layout.addWidget(label_prenom)
        self.__frist_layout.addWidget(self.profil_informations.prenom)

        label_age = CustomLabelName("Age :")
        self.__frist_layout.addWidget(label_age)
        self.__frist_layout.addWidget(self.profil_informations.age)

        # ==============================================================================================================
        # Profession, salaire, situation matrimoniale.
        # ==============================================================================================================
        label_profession = CustomLabelName("Profession :")
        self.__second_layout.addWidget(label_profession)
        self.__second_layout.addWidget(self.profil_informations.profession)

        label_salaire = CustomLabelName("Salaire / Bourse mensuelle :")
        self.__second_layout.addWidget(label_salaire)
        self.__second_layout.addWidget(self.profil_informations.salaire)

        label_matrimoniale = CustomLabelName("Situation matrimoniale :")
        self.__second_layout.addWidget(label_matrimoniale)
        self.__second_layout.addWidget(self.profil_informations.matrimoniale)

        # ==============================================================================================================
        # Pays de résidence/smig, Pays sinistre/smig, smig retenu.
        # ==============================================================================================================
        label_pays_r = CustomLabelName("Pays de résidence/SMIG :")
        self.__thrid_layout.addWidget(label_pays_r)
        self.__thrid_layout.addWidget(self.profil_informations.pays_residence)

        label_pays_s = CustomLabelName("Pays lieu du sinistre/SMIG :")
        self.__thrid_layout.addWidget(label_pays_s)
        self.__thrid_layout.addWidget(self.profil_informations.pays_sinistre)

        label_smig = CustomLabelName("SMIG Retenu :")
        self.__thrid_layout.addWidget(label_smig)
        self.__thrid_layout.addWidget(self.profil_informations.smig_retenu)

        # Chargement du profil de la victime.
        self.load_profil_dead()

        # Enregistrement de la méthode d'appel.
        data_contoller.add_callable_function(key="load_profil_dead", func=self.load_profil_dead)
        data_contoller.add_callable_function(key="close_profil_dead", func=self.close())

    def load_profil_dead(self):
        from api import laod_default_personne_dead
        print("--------------------------------------------------------------")
        default_personne = laod_default_personne_dead()
        print("Chargement du profil... : Personne :", default_personne.nom)
        try:
            # Récupérer depuis le data_controller
            self.profil_informations.nom.setText(default_personne.nom)
            self.profil_informations.prenom.setText(default_personne.prenom)
            self.profil_informations.age.setText(f"{default_personne.age} ans")

            self.profil_informations.profession.setText(default_personne.profession)
            self.profil_informations.salaire.setText(f"{format_nombre_fr(default_personne.salaire)} F CFA")
            self.profil_informations.matrimoniale.setText(default_personne.situation_matrimoniale)

            # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
            smig_residence = smig_pays_cima_2025.get(default_personne.pays_residence)
            smig_sinistre = smig_pays_cima_2025.get(default_personne.pays_sinistre)

            # Définition du smig à retenir pour le calcul du plafond et des indemnités.
            smig = max(smig_residence,
                       smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

            self.profil_informations.pays_residence.setText(
                f"{default_personne.pays_residence} / {format_nombre_fr(smig_residence)} F CFA")
            self.profil_informations.pays_sinistre.setText(
                f"{default_personne.pays_sinistre} / {format_nombre_fr(smig_sinistre)} F CFA")
            self.profil_informations.smig_retenu.setText(f"{format_nombre_fr(smig)} F CFA")

            print("Fin du chargement du profil... Personne :", default_personne.nom)
            print("--------------------------------------------------------------")
        except Exception as e:
            error_logger.log_error(message=e, exception=e)
            print(e)

        # Afin de pouvoir restaurer la dernière fenêtre.
        data_contoller.load_profil_alive = False
        pass

        # ==============================================================================================================
        # ==============================================================================================================

    # Cette classe sera le domaine qui contiendra tous les bouttons de ce widget.
    class ButtonGroup:
        def __init__(self):
            self.modifier_profile = QPushButton("Charger profil 🖊️")
            self.modifier_profile.setFixedSize(250, 30)
            self.modifier_profile.setStyleSheet("""
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

            self.modifier_profile.clicked.connect(self.charger_profil)

        def charger_profil(self):
            charger_profil = ListProfilsDead()
            charger_profil.show()
            charger_profil.exec()

        pass

    class ProfilInformations:
        def __init__(self):
            self.nom = ProfilLabel("-")
            self.prenom = ProfilLabel("-")
            self.age = ProfilLabel("-")

            self.profession = ProfilLabel("-")
            self.salaire = ProfilLabel("-")
            self.matrimoniale = ProfilLabel("-")

            self.pays_residence = ProfilLabel("-")
            self.pays_sinistre = ProfilLabel("-")
            self.smig_retenu = ProfilLabel("-")

    pass


class FraisWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Frais Médicaux")

        self.add_content(QLabel("Cumul des frais médicaux pris en charge par l'assurance\n(sans les espaces) :"))
        self.cumul_line_edit = QLineEdit()
        self.cumul_line_edit.setPlaceholderText("000 000 000 F CFA")
        self.add_content(self.cumul_line_edit)

        self.__red_label = QLabel("Entrée invalide. Veuillez entrer une valeur numérique !")
        self.__red_label.setStyleSheet("font-size: 15; font-weight: bold; color: #D20F45;")
        self.__red_label.hide()
        self.add_content(self.__red_label)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(7):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        self.cumul_line_edit.editingFinished.connect(self.focus_out_or_entry)

    def focus_out_or_entry(self):
        valeur = self.cumul_line_edit.text()
        frais_de_traitment = FraisDeTraitement()

        if not valeur:
            pass

        try:
            valeur_int = int(valeur)
            self.__red_label.hide()
            frais_de_traitment.valeur = valeur_int
            indemnite = frais_de_traitment.valeur
            self.lbl_result.setText(f"{format_nombre_fr(indemnite)} F CFA")
        except:
            self.__red_label.show()
            self.lbl_result.setText("000 000 000 F CFA")
            return
        pass
    pass


class IncapaciteWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Incapacité Temporaire / Permanente")

        self.add_content(QLabel("Type d'incapacité :"))
        self.type_combobox = QComboBox()
        self.type_combobox.addItems(["Incapacité Temporaire", "Incapacité Permanente"])
        self.type_combobox.currentTextChanged.connect(self.change_widget)
        self.add_content(self.type_combobox)

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        # Créations des sous widgets.
        self.it_widget = QWidget()
        self.ip_widget = QWidget()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.it_widget)
        self.stacked_widget.addWidget(self.ip_widget)
        self.stacked_widget.setCurrentWidget(self.it_widget)
        self.add_content(self.stacked_widget)

        # Définir le contenu de chaque widget.
        # WIdget IT.
        self.label = QLabel("Incapacité Temporaire")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        color: #31588A;
                        margin-bottom: 3px;
                        font-size: 14px;
                    }
                """)
        self.it_line_edit = QLineEdit()
        self.it_line_edit.setMinimumHeight(20)
        self.it_line_edit.setPlaceholderText("Taux: 0 - 100")
        self.duree_line_edit = QLineEdit()
        self.duree_line_edit.setMinimumHeight(20)
        self.duree_line_edit.setPlaceholderText("Durée en jours")

        self.it_layout = QVBoxLayout(self.it_widget)
        self.it_layout.addWidget(self.label)
        self.it_layout.addWidget(QLabel("Taux d'IT :"))
        self.it_layout.addWidget(self.it_line_edit)
        self.it_layout.addWidget(QLabel("Durée (Jours) :"))
        self.it_layout.addWidget(self.duree_line_edit)

        self.__red_label_it = QLabel("Entrée invalide. 0 < Taux d'IT < 100 ! Dureé >= 0 jrs")
        self.__red_label_it.setStyleSheet("font-size: 15; font-weight: bold; color: #D20F45;")
        self.__red_label_it.hide()
        self.it_layout.addWidget(self.__red_label_it)

        # WIdget IP.
        self.label = QLabel("Incapacité Permanente")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        color: #31588A;
                        margin-bottom: 3px;
                        font-size: 14px;
                    }
                """)
        self.ip_line_edit = QLineEdit()
        self.ip_line_edit.setMinimumHeight(20)
        self.ip_line_edit.setPlaceholderText("Taux: 0 - 100")
        self.salaire_apres_accident_line_edit = QLineEdit()
        self.salaire_apres_accident_line_edit.setMinimumHeight(20)
        self.salaire_apres_accident_line_edit.setPlaceholderText("000 000 000 F CFA")

        self.ip_layout = QVBoxLayout(self.ip_widget)
        self.ip_layout.addWidget(self.label)
        self.ip_layout.addWidget(QLabel("Taux d'IP :"))
        self.ip_layout.addWidget(self.ip_line_edit)
        self.ip_layout.addWidget(QLabel("Le salaire après l'accident (sans les espaces) :"))
        self.ip_layout.addWidget(self.salaire_apres_accident_line_edit)

        self.__red_label_ip = QLabel("Entrée invalide. 0 < Taux d'IT < 100 ! Salaire >= 0")
        self.__red_label_ip.setStyleSheet("font-size: 15; font-weight: bold; color: #D20F45;")
        self.__red_label_ip.hide()
        self.ip_layout.addWidget(self.__red_label_ip)

        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)


        lbl = QLabel("Indemnité (Totale dans le cas de l'IP) :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        self.it_line_edit.textChanged.connect(self.it_result)
        self.duree_line_edit.textChanged.connect(self.it_result)

        self.ip_line_edit.textChanged.connect(self.ip_result)
        self.salaire_apres_accident_line_edit.textChanged.connect(self.ip_result)


    def change_widget(self, current_text):
        if current_text == "Incapacité Temporaire":
            self.stacked_widget.setCurrentWidget(self.it_widget)
            return
        self.stacked_widget.setCurrentWidget(self.ip_widget)

    def it_result(self):
        personne: Personne = laod_default_personne_alive()

        taux_it = self.it_line_edit.text()
        duree_it = self.duree_line_edit.text()

        if not taux_it or not duree_it:
            pass

        try:
            taux_it_int = int(taux_it)
            duree_it_int = int(duree_it)

            if taux_it_int > 100:
                self.__red_label_it.show()
                return

            self.__red_label_it.hide()
            incapacite_temporaire = IncapaciteTemporaire(personne=personne, duree=duree_it_int, taux_it=taux_it_int)
            indemnite = incapacite_temporaire.incapacite_temporaire_partielle()
            self.lbl_result.setText(f"{format_nombre_fr(indemnite)} F CFA")
        except:
            self.__red_label_it.show()
            self.lbl_result.setText("000 000 000 F CFA")
            return

        pass

    def ip_result(self):
        personne: Personne = laod_default_personne_alive()

        taux_ip = self.ip_line_edit.text()
        salaire_apres_sinistre = self.salaire_apres_accident_line_edit.text()

        if not taux_ip or not salaire_apres_sinistre:
            pass

        try:
            taux_ip_int = int(taux_ip)
            salaire_apres_sinistre_int = int(salaire_apres_sinistre)

            if taux_ip_int > 100:
                self.__red_label_ip.show()
                return

            self.__red_label_ip.hide()

            if salaire_apres_sinistre_int > personne.salaire:
                QMessageBox.critical(None, "Erreur", f"Le nouveau salaire après le sinistre est \nsupérieur au salaire de la victime.\nEchec de l'enrégistrement.")
                return

            incapacite_permanente = IncapacitePermanente(personne=personne, taux_ip=taux_ip_int, salaire_apres_accident=salaire_apres_sinistre_int)
            indemnite = incapacite_permanente.valeur()
            self.lbl_result.setText(f"{format_nombre_fr(indemnite)} F CFA")

            # Détermination du SMIG du pays de résidence et du pays lieu du sinistre.
            smig_residence = int(smig_pays_cima_2025.get(personne.pays_residence))
            smig_sinistre = int(smig_pays_cima_2025.get(personne.pays_sinistre))

            # Définition du smig à retenir pour le calcul du plafond et des indemnités.
            smig = max(smig_residence,
                       smig_sinistre)  # Le plus grand des deux smig selon les dispositions du Code CIMA.

            # À suivre...
            data_contoller.save_data(key="taux_ip", value=taux_ip_int)
            data_contoller.save_data(key="indemnite_ip", value=indemnite)
            data_contoller.save_data(key="prejudice_economique", value=incapacite_permanente.prejudice_economique())
            data_contoller.save_data(key="prejudice_physiologique", value=incapacite_permanente.prejudice_physiologique())
            data_contoller.save_data(key="prejudice_moral", value=incapacite_permanente.prejudice_moral())
            data_contoller.save_data(key="smig_annuel", value=12 * smig)
            data_contoller.save_data(key="salaire_apres_sinistre", value=salaire_apres_sinistre_int)

            # Loading extra functions for printing others results.
            data_contoller.call_fonction(key="calculate_prejduice_economique")
            data_contoller.call_fonction(key="calculate_prejduice_physiologique")
            data_contoller.call_fonction(key="calculate_prejduice_moral")
            data_contoller.call_fonction(key="calculate_assistance_tierce_personne")
            data_contoller.call_fonction(key="prejudice_moral_conjoint")
        except Exception as e:
            print(e)
            self.__red_label_ip.show()
            self.lbl_result.setText("000 000 000 F CFA")
            return

        pass

    pass


class PrejudiceEconomiqueWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Prejudice économique")

        self.add_content(QLabel("Taux d'IP (>=50%) : "))

        self.niveau_it = QLabel("-")
        self.niveau_it.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.niveau_it)

        self.add_content(QLabel("SMIG annuel :"))
        self.lbl_smig_annuel_result = QLabel("- F CFA")
        self.lbl_smig_annuel_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_smig_annuel_result)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(7):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        data_contoller.add_callable_function(key="calculate_prejduice_economique", func=self.calculate_prejduice_economique)

    def calculate_prejduice_economique(self):
        self.niveau_it.setText(f"{data_contoller.load_data(key='taux_ip')}%")
        self.lbl_smig_annuel_result.setText(f"{format_nombre_fr(data_contoller.load_data(key='smig_annuel'))} F CFA")
        self.lbl_result.setText(f"{format_nombre_fr(data_contoller.load_data(key='prejudice_economique'))} F CFA")
        pass

    pass


class PrejudiceMoralWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Prejudice moral")

        self.add_content(QLabel("Taux d'IP (>=80%) : "))

        self.niveau_it = QLabel("-")
        self.niveau_it.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.niveau_it)

        self.add_content(QLabel("SMIG annuel :"))
        self.lbl_smig_annuel_result = QLabel("- F CFA")
        self.lbl_smig_annuel_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_smig_annuel_result)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(7):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        data_contoller.add_callable_function(key="calculate_prejduice_moral", func=self.calculate_prejduice_moral)

    def calculate_prejduice_moral(self):
        self.niveau_it.setText(f"{data_contoller.load_data(key='taux_ip')}%")
        self.lbl_smig_annuel_result.setText(f"{format_nombre_fr(data_contoller.load_data(key='smig_annuel'))} F CFA")
        self.lbl_result.setText(f"{format_nombre_fr(data_contoller.load_data(key='prejudice_moral'))} F CFA")
        pass

    pass


class PrejudicePhysiologiqueWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Prejudice physiologique")

        self.add_content(QLabel("Taux d'IP : "))

        self.niveau_it = QLabel("-")
        self.niveau_it.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.niveau_it)

        self.add_content(QLabel("SMIG annuel :"))
        self.lbl_smig_annuel_result = QLabel("- F CFA")
        self.lbl_smig_annuel_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_smig_annuel_result)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(7):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        data_contoller.add_callable_function(key="calculate_prejduice_physiologique",
                                             func=self.calculate_prejduice_physiologique)

    def calculate_prejduice_physiologique(self):
        self.niveau_it.setText(f"{data_contoller.load_data(key='taux_ip')}%")
        self.lbl_smig_annuel_result.setText(
            f"{format_nombre_fr(data_contoller.load_data(key='smig_annuel'))} F CFA")
        self.lbl_result.setText(f"{format_nombre_fr(data_contoller.load_data(key='prejudice_physiologique'))} F CFA")
        pass

    pass


class AssistanceTiercePersonneWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Assistance d'une tierce personne")

        self.assistance_checkbox = QCheckBox("La victime a-t-elle besoin de l'assistance d'une\ntierce personne ?")
        self.add_content(self.assistance_checkbox)

        self.add_content(QLabel("Indemnité totale au titre de l'IP :"))
        self.lbl_ip_result = QLabel("- F CFA")
        self.lbl_ip_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_ip_result)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(5):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        self.assistance_checkbox.checkStateChanged.connect(self.calculate_assistance_tierce_personne)
        data_contoller.add_callable_function(key="calculate_assistance_tierce_personne",
                                             func=self.calculate_assistance_tierce_personne)

    def calculate_assistance_tierce_personne(self):
        try:
            if not self.assistance_checkbox.isChecked():
                self.lbl_result.setText("000 000 000 F CFA")
                return
            personne = laod_default_personne_alive()
            assistance_tp = AssistanceTiercePersonne(personne=personne,
                                                     taux_ip=int(data_contoller.load_data(key="taux_ip")),
                                                     salaire_apres_accident=int(data_contoller.load_data(key="salaire_apres_sinistre")))
            self.lbl_ip_result.setText(f"{format_nombre_fr(data_contoller.load_data(key='indemnite_ip'))} F FCA")
            self.lbl_result.setText(f"{format_nombre_fr(assistance_tp.valeur())} F CFA")
        except:
            print("Checked !")
            print("calculate_assistance_tierce_personne - Something's wrong !")
            return
    pass


class PretiumDolorisWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Pretium doloris")

        from algorithm.tables import NiveauPrejudice

        self.add_content(QLabel("Niveau du préjudice : "))

        self.niveau_checkbox = QComboBox()
        self.niveau_checkbox.addItems(["-",
                                       f"Très léger : {NiveauPrejudice().tres_leger}%",
                                       f"Léger : {NiveauPrejudice().leger}%",
                                       f"Modéré : {NiveauPrejudice().modere}%",
                                       f"Moyen : {NiveauPrejudice().moyen}%",
                                       f"Assez important : {NiveauPrejudice().assez_important}%",
                                       f"Important : {NiveauPrejudice().important}%",
                                       f"Très important : {NiveauPrejudice().tres_important}%",
                                       f"Exceptionnel : {NiveauPrejudice().exceptionnel}%", ])
        self.add_content(self.niveau_checkbox)

        self.add_content(QLabel("SMIG annuel :"))
        self.lbl_smig_annuel_result = QLabel("- F CFA")
        self.lbl_smig_annuel_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_smig_annuel_result)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(6):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        self.niveau_checkbox.currentTextChanged.connect(self.indemnite_pretium_or_esthetique)

    def niveau_prejudice(self, niveau: str) -> int:
        match niveau:
            case "-":
                return 0
            case "Très léger : 5%":
                return NiveauPrejudice().tres_leger
            case "Léger : 10%":
                return NiveauPrejudice().leger
            case "Modéré : 20%":
                return NiveauPrejudice().modere
            case "Moyen : 40%":
                return NiveauPrejudice().moyen
            case "Assez important : 60%":
                return NiveauPrejudice().assez_important
            case "Important : 100%":
                return NiveauPrejudice().important
            case "Très important : 150%":
                return NiveauPrejudice().tres_important
            case "Exceptionnel : 300%":
                return NiveauPrejudice().exceptionnel
        return 0

    def indemnite_pretium_or_esthetique(self, niveau: str):
        try:
            personne = laod_default_personne_alive()
            prejudice = PretiumDoloris(personne=personne, niveau=self.niveau_prejudice(niveau=niveau))
            self.lbl_smig_annuel_result.setText(f"{format_nombre_fr(prejudice.smig * 12)} F CFA")
            self.lbl_result.setText(f"{format_nombre_fr(prejudice.valeur())} F CFA")
        except:
            return
        pass

    pass


class PrejudiceEsthetiqueWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Préjudice esthétique :")

        from algorithm.tables import NiveauPrejudice

        self.add_content(QLabel("Niveau du préjudice : "))

        self.niveau_checkbox = QComboBox()
        self.niveau_checkbox.addItems(["-",
                                       f"Très léger : {NiveauPrejudice().tres_leger}%",
                                       f"Léger : {NiveauPrejudice().leger}%",
                                       f"Modéré : {NiveauPrejudice().modere}%",
                                       f"Moyen : {NiveauPrejudice().moyen}%",
                                       f"Assez important : {NiveauPrejudice().assez_important}%",
                                       f"Important : {NiveauPrejudice().important}%",
                                       f"Très important : {NiveauPrejudice().tres_important}%",
                                       f"Exceptionnel : {NiveauPrejudice().exceptionnel}%", ])
        self.add_content(self.niveau_checkbox)

        self.add_content(QLabel("SMIG annuel :"))
        self.lbl_smig_annuel_result = QLabel("- F CFA")
        self.lbl_smig_annuel_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_smig_annuel_result)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(6):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        self.niveau_checkbox.currentTextChanged.connect(self.indemnite_pretium_or_esthetique)

    def niveau_prejudice(self, niveau: str) -> int:
        match niveau:
            case "-":
                return 0
            case "Très léger : 5%":
                return NiveauPrejudice().tres_leger
            case "Léger : 10%":
                return NiveauPrejudice().leger
            case "Modéré : 20%":
                return NiveauPrejudice().modere
            case "Moyen : 40%":
                return NiveauPrejudice().moyen
            case "Assez important : 60%":
                return NiveauPrejudice().assez_important
            case "Important : 100%":
                return NiveauPrejudice().important
            case "Très important : 150%":
                return NiveauPrejudice().tres_important
            case "Exceptionnel : 300%":
                return NiveauPrejudice().exceptionnel
        return 0

    def indemnite_pretium_or_esthetique(self, niveau: str):
        try:
            personne = laod_default_personne_alive()
            prejudice = PrejudiceEsthetique(personne=personne, niveau=self.niveau_prejudice(niveau=niveau))
            self.lbl_smig_annuel_result.setText(f"{format_nombre_fr(prejudice.smig * 12)} F CFA")
            self.lbl_result.setText(f"{format_nombre_fr(prejudice.valeur())} F CFA")
        except:
            return
        pass

    pass


class PerteGainsProFuturWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Perte de gains professionnels futur")

        self.niveau_checkbox = QCheckBox("Y'a-t-il perte de gains professionnels futur ?")
        self.add_content(self.niveau_checkbox)

        self.add_content(QLabel("Salaire sur les 6 mois :"))
        self.lbl_salaire_six_mois = QLabel("- F CFA")
        self.lbl_salaire_six_mois.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_salaire_six_mois)

        self.add_content(QLabel("Plafond :"))
        self.lbl_plafond = QLabel("- F CFA")
        self.lbl_plafond.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_plafond)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(5):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        self.niveau_checkbox.checkStateChanged.connect(self.perte_de_gains_pro_futur)

    def perte_de_gains_pro_futur(self):
        if not self.niveau_checkbox.isChecked():
            self.lbl_salaire_six_mois.setText("- F CFA")
            self.lbl_plafond.setText("- F CFA")
            self.lbl_result.setText("000 000 000 F CFA")
            return

        try:
            personne = laod_default_personne_alive()
            prejudice = PrejudicePerteDeGainsProfessinnelsFuturs(personne=personne)
            self.lbl_salaire_six_mois.setText(f"{format_nombre_fr(personne.salaire * 6)} F CFA")
            self.lbl_plafond.setText(f"{format_nombre_fr(prejudice.plafond)} F CFA")
            self.lbl_result.setText(f"{format_nombre_fr(prejudice.valeur())} F CFA")
        except:
            return
        pass

    pass


class PrejudiceScolaireWidget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Préjudice scolaire")

        self.niveau_checkbox = QCheckBox("Y'a-t-il un préjudice scolaire ?")
        self.add_content(self.niveau_checkbox)

        self.add_content(QLabel("Bourse mensuelle officiel :"))
        self.lbl_bourse = QLabel("- F CFA")
        self.lbl_bourse.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_bourse)

        self.add_content(QLabel("Bourse annuel :"))
        self.lbl_plafond = QLabel("- F CFA")
        self.lbl_plafond.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_plafond)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(5):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        self.niveau_checkbox.checkStateChanged.connect(self.prejudice_scolaire)

    def prejudice_scolaire(self):
        if not self.niveau_checkbox.isChecked():
            self.lbl_bourse.setText("- F CFA")
            self.lbl_plafond.setText("- F CFA")
            self.lbl_result.setText("000 000 000 F CFA")
            return

        try:
            personne = laod_default_personne_alive()
            prejudice = PrejudiceScolaire(personne=personne)
            self.lbl_bourse.setText(f"{format_nombre_fr(prejudice.bourse_officielle)} F CFA")
            self.lbl_plafond.setText(f"{format_nombre_fr(prejudice.bourse_officielle * 12)} F CFA")
            self.lbl_result.setText(f"{format_nombre_fr(prejudice.valeur())} F CFA")
        except:
            return
        pass

    pass


class PrejudiceMoralConjointWIdget(CustomCalculusQWidget):
    def __init__(self):
        super().__init__(intitule="Préjudice moral du conjoint")

        self.add_content(QLabel("Situation matrimoniale :"))
        self.lbl_sit_mat = QLabel("-")
        self.lbl_sit_mat.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_sit_mat)

        self.add_content(QLabel("Taux d'IP :"))
        self.lbl_taux = QLabel("-")
        self.lbl_taux.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_taux)

        # Contenu vide pour ajuster la disposition de tous les widgets.
        for i in range(7):
            self.add_content(QLabel())

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.add_content(self.__separator)

        lbl = QLabel("Indemnité :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.add_content(lbl)

        self.lbl_result = QLabel("000 000 000 F CFA")
        self.lbl_result.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_result.setStyleSheet("font-size: 15; font-weight: bold; color: #31588A;")
        self.add_content(self.lbl_result)

        data_contoller.add_callable_function(key="prejudice_moral_conjoint", func=self.prejudice_moral_conjoint)

    def prejudice_moral_conjoint(self):
        from algorithm.profils import Personne
        personne: Personne = laod_default_personne_alive()

        if not personne.conjoints:
            self.lbl_taux.setText("Doit être égal à 100%")
            self.lbl_sit_mat.setText("Doit avoir au moins 1 conjoint.")
            self.lbl_result.setText("000 000 000 F CFA")
            print("Personne sans conjoint.s:")
            return

        print("Personne mariée, nombres de conjoint.s:", len(personne.conjoints))

        try:
            taux_ip = data_contoller.load_data(key="taux_ip")

            if int(taux_ip) != 100:
                self.lbl_taux.setText("-%")
                self.lbl_sit_mat.setText("-")
                self.lbl_result.setText("000 000 000 F CFA")
                print("Taux d'IP invalide:", taux_ip, "%")
                return

            print("Taux d'IP valide:", taux_ip, "%")
            self.lbl_sit_mat.setText(f"{len(personne.conjoints)} conjoint.s")
            self.lbl_taux.setText(f"{taux_ip}%")

            try:
                prejudice = PrejudiceMoralConjoint(personne=personne, taux_ip=int(taux_ip))
                print(f"Préjudice moral du conjoint : {format_nombre_fr(prejudice.valeur())} F CFA")
                self.lbl_result.setText(f"{format_nombre_fr(prejudice.valeur())} F CFA")
            except Exception as e:
                print(e)

        except:
            self.lbl_taux.setText("Doit être égal à 100%")
            self.lbl_sit_mat.setText("Doit avoir au moins 1 conjoint.")
            self.lbl_result.setText("000 000 000 F CFA")
            return
        pass

    pass


class ItIpWidget(ScrollableWidget):
    def __init__(self):
        super().__init__()

        # Calcul de la largeur nécessaire (8 widgets de 350px + espacements)
        total_width = 8 * 350 + 7 * 20  # 7 espacements entre 8 widgets
        self.container.setMinimumWidth(total_width)

        widgets = [
            FraisWidget(), IncapaciteWidget(),
            PrejudiceEconomiqueWidget(),
            PrejudicePhysiologiqueWidget(),
            PrejudiceMoralWidget(),
            AssistanceTiercePersonneWidget(),
            PretiumDolorisWidget(),
            PrejudiceEsthetiqueWidget(),
            PerteGainsProFuturWidget(),
            PrejudiceScolaireWidget(),
            PrejudiceMoralConjointWIdget()
        ]

        for widget in widgets:
            wrapped = WidgetContainer(widget)
            self.container_layout.addWidget(wrapped)

        # Option : ajouter un stretch à la fin si nécessaire
        self.container_layout.addStretch()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RepartitionEnfants(RepartitionWidget):
    def __init__(self):
        from api import laod_default_personne_dead

        self.personne = laod_default_personne_dead()

        height = max(len(self.personne.enfants), len(self.personne.conjoints), len(self.personne.ascendants),
                     len(self.personne.collateraux))

        super().__init__(intitule="Enfants", list_ayants_droit=self.personne.enfants, height=height)
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
                        """)

        data_contoller.add_callable_function("load_repartition_enfants", self.load_repartition_enfants)

    def load_repartition_enfants(self):
        print("Reloading load_repartition_enfants...")
        pass
    pass


class RepartitionConjoints(RepartitionWidget):
    def __init__(self):
        from api import laod_default_personne_dead

        self.personne = laod_default_personne_dead()

        height = max(len(self.personne.enfants), len(self.personne.conjoints), len(self.personne.ascendants),
                     len(self.personne.collateraux))

        super().__init__(intitule="Conjoints", list_ayants_droit=self.personne.conjoints, height=height)

        data_contoller.add_callable_function("load_repartition_conjoints", self.load_repartition_conjoints)

    def load_repartition_conjoints(self):
        print("Reloading load_repartition_conjoints...")
        pass
    pass


class RepartitionAscendants(RepartitionWidget):
    def __init__(self):
        from api import laod_default_personne_dead

        self.personne = laod_default_personne_dead()

        height = max(len(self.personne.enfants), len(self.personne.conjoints), len(self.personne.ascendants),
                     len(self.personne.collateraux))

        super().__init__(intitule="Ascendants", list_ayants_droit=self.personne.ascendants, height=height)

        data_contoller.add_callable_function("load_repartition_ascendants", self.load_repartition_ascendants)

    def load_repartition_ascendants(self):
        print("Reloading load_repartition_ascendants...")
        pass
    pass


class RepartitionCollateraux(RepartitionWidget):
    def __init__(self):
        from api import laod_default_personne_dead

        self.personne = laod_default_personne_dead()

        height = max(len(self.personne.enfants), len(self.personne.conjoints), len(self.personne.ascendants),
                     len(self.personne.collateraux))
        super().__init__(intitule="Collatéraux", list_ayants_droit=self.personne.collateraux, height=height)

        data_contoller.add_callable_function("load_repartition_collateraux", self.load_repartition_collateraux)

    def load_repartition_collateraux(self):
        print("Reloading load_repartition_collateraux...")
        pass
    pass


class RepartitionAyantsDroitWidget(ScrollableWidget):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(300)
        # self.container.setMinimumWidth(total_width)
        self.container.setFixedWidth(2200)

        widgets = [
            RepartitionEnfants(),
            RepartitionConjoints(),
            RepartitionAscendants(),
            RepartitionCollateraux()
        ]

        for widget in widgets:
            self.container_layout.addWidget(widget)

        # Option : ajouter un stretch à la fin si nécessaire
        self.container_layout.addStretch()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class VictimeBlessee(QWidget):
    def __init__(self):
        super().__init__()
        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(10)  # Espacement entre les widgets

        label_ayants_droit = QLabel("La victime blessée")
        label_ayants_droit.setStyleSheet("""
                                    QLabel {
                                        color: #34495e;
                                        font-size: 16px;
                                        font-weight: bold;
                                        padding-bottom: 8px;
                                        border-bottom: 2px solid #3498db;  /* Ligne de séparation bleue */
                                        margin-bottom: 7px;
                                    }
                                """)
        label_ayants_droit.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__main_layout.addWidget(label_ayants_droit)

        # Widgets
        self.__profile_widget = ProfilAlive()
        self.__it_ip_page = ItIpWidget()

        # Ajout avec facteur d'étirement
        self.__main_layout.addWidget(self.__profile_widget, stretch=0)

        label_ayants_droit = QLabel("Différentes Indemnités")
        label_ayants_droit.setStyleSheet("""
                                                    QLabel {
                                                        color: #34495e;
                                                        font-size: 16px;
                                                        font-weight: bold;
                                                        padding-bottom: 8px;
                                                        border-bottom: 2px solid #3498db;  /* Ligne de séparation bleue */
                                                        margin-bottom: 7px;
                                                    }
                                                """)
        label_ayants_droit.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__main_layout.addWidget(label_ayants_droit)

        self.__main_layout.addWidget(self.__it_ip_page, stretch=1)  # Prend tout l'espace restant


class VictimeDecedee(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: transparent;")

        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(10)  # Espacement entre les widgets

        self.main_widget = QWidget(self)
        self.__main_layout.addWidget(self.main_widget)



        self.profil_widget = ProfilDead()

        self.container_layout = QVBoxLayout(self.main_widget)

        # Ajout d'un layout pour les profils des ayants droit de la victime.
        label_ayants_droit = QLabel("La victime décédée")
        label_ayants_droit.setStyleSheet("""
                            QLabel {
                                color: #34495e;
                                font-size: 16px;
                                font-weight: bold;
                                padding-bottom: 8px;
                                border-bottom: 2px solid #3498db;  /* Ligne de séparation bleue */
                                margin-bottom: 7px;
                            }
                        """)
        label_ayants_droit.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.container_layout.addWidget(label_ayants_droit)

        self.container_layout.addWidget(self.profil_widget, stretch=0)

        """
        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(7)
        # self.__separator.setFixedWidth(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.container_layout.addWidget(self.__separator)
        """

        # Ajout d'un layout pour les profils des ayants droit de la victime.
        label_ayants_droit = QLabel("Les ayants droits")
        label_ayants_droit.setStyleSheet("""
                            QLabel {
                                color: #34495e;
                                font-size: 16px;
                                font-weight: bold;
                                padding-bottom: 8px;
                                border-bottom: 2px solid #3498db;  /* Ligne de séparation bleue */
                                margin-bottom: 7px;
                            }
                        """)
        label_ayants_droit.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.container_layout.addWidget(label_ayants_droit)

        # Le widget qui est censé afficher les résultats.
        self.repartition_ayants_droit = RepartitionAyantsDroitWidget()
        self.container_layout.addWidget(self.repartition_ayants_droit, stretch=1)

        data_contoller.add_callable_function("recreate_repartition", self.recreate_repartition)

    def suprrimer_repartition_widget(self):
        self.container_layout.removeWidget(self.repartition_ayants_droit)
        pass

    def recreate_repartition(self):
        # On supprime le widget de répartition afin de le recréer et de le replacer.
        self.suprrimer_repartition_widget()
        # Le widget qui est censé afficher les résultats.
        self.repartition_ayants_droit = RepartitionAyantsDroitWidget()
        print("Chargement effectué avec succès...")
        self.container_layout.addWidget(self.repartition_ayants_droit, stretch=1)
        pass

    pass


class GestionGroupe(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(255, 255, 100);")

        self.__main_layout = QVBoxLayout(self)

        self.main_widget = QWidget(self)
        self.__main_layout.addWidget(self.main_widget)
    pass
