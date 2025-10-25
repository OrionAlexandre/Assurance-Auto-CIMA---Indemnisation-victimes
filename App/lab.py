import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QMessageBox, QDialog, \
    QGridLayout, QLineEdit, QComboBox, QStackedLayout, QListView, QStackedWidget, QCheckBox, QPushButton, QMenu, \
    QTextEdit

from algorithm.dead import PrejudiceEconomiqueConjoints, ControlePlafondPrejudiceEconomique, PrejudiceEconomiqueEnfants,\
    PrejudiceMoral, ControlePlafondPrejudiceMoral
from algorithm.profils import Enfant, Conjoint, Personne, Ascendant, Collateral

from algorithm.tables import SituationMatrimoniale, AGE_LIMITE, list_pays_cima, ValeurPointIP, TableTemporaire65, TableTemporaire60, TableTemporaire55, TableTemporaire25, TableTemporaire21
from database_manager import ajouter_personne_data_base, supprimer_et_reorganiser_ids
from api import data_contoller


app = QApplication(sys.argv)


class TableRentesPermanenteWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Table des rentes viagères")
        icon = QIcon(QPixmap("assets/064-browsers.png"))
        self.setWindowIcon(icon)
        self.setModal(True)

        self.main_layout = QVBoxLayout(self)

        self.setStyleSheet("""
                                            QWidget {
                                                background-color: qlineargradient(
                                                        x1:0, y1:0, x2:1, y2:1,
                                                        stop:0 #B9D5F9,
                                                        stop:0.6 #e8f2ff,
                                                        stop:1 #d0e3ff
                                                    );
                                            }

                                            QLabel {
                                                background-color: transparent;
                                                color: #31588A;
                                                margin-bottom: 3px;
                                                font-size: 14px;
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

        # Ajout d'un layout pour les profils des ayants droit de la victime.
        self.label_ = QLabel("Age limite du paiement de la rente : 65 ans")
        self.label_.setStyleSheet("""
                                                    QLabel {
                                                        color: #34495e;
                                                        font-size: 16px;
                                                        font-weight: bold;
                                                        padding-bottom: 8px;
                                                        border-bottom: 2px solid #3498db;  /* Ligne de séparation bleue */
                                                        margin-bottom: 7px;
                                                    }
                                                """)
        self.label_.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.label_)

        self.entries = self.Entries(title=self.label_)

        choose_age_layout = QHBoxLayout()
        self.main_layout.addLayout(choose_age_layout)
        label_ = QLabel("Age limite du paiement de la rente : ")
        # label_.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        choose_age_layout.addWidget(label_)
        choose_age_layout.addWidget(self.entries.age_limite_entry)

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        # self.__separator.setFixedWidth(1)
        self.__separator.setStyleSheet("background-color: #060270; margin-top: 3px; margin-bottom: 7px;")
        self.main_layout.addWidget(self.__separator)

        widget_layout = QGridLayout()
        self.main_layout.addLayout(widget_layout)

        row, col = 0, 0
        for label in self.entries.labels():
            widget_layout.addWidget(label, row, col)
            col += 1

        row, col = 1, 0
        for entry in self.entries.entries():
            widget_layout.addWidget(entry, row, col)
            col += 1

    class Entries:
        def __init__(self, title: QLabel):
            self.current_age_limite_table = TableTemporaire65

            self.title = title
            self.age_limite_entry = QComboBox()

            self.age_entry = QLineEdit()
            self.sexe_entry = QComboBox()
            self.output_entry = QLineEdit()

            self.__label_age = QLabel("L'âge du profil :")
            self.__label_tip = QLabel("Sexe du profil :")
            self.__label_output = QLabel("Barème de capitalisation :")

            self.output_entry.setReadOnly(True)
            self.age_entry.setText(f"{0}")
            self.sexe_entry.addItems(["M", "F"])

            self.age_limite_entry.addItems(["65", "60", "55" ,"25", "21"])

            self.default_personne: Personne = Personne(
                nom="-",
                prenom="-",
                age=0,
                sexe="M",
                profession="-",
                salaire=0.0,
                age_limite=60,
                situation_matrimoniale=SituationMatrimoniale.CELIBATAIRE,
                conjoints=[],
                enfants=[],
                ascendants=[],
                collateraux=[],
                pays_residence="Togo",
                pays_sinistre="Togo",
            )
            self.output_entry.setText(f"{TableTemporaire65(personne=self.default_personne).bareme()}")

            self.__set_style()
            self.age_entry.textChanged.connect(self.__age_changed)
            self.sexe_entry.currentTextChanged.connect(self.__sexe_changed)
            self.age_limite_entry.currentTextChanged.connect(self.__age_limite_changed)

        def __set_style(self):
            self.age_entry.setStyleSheet("""
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
                            """)
            self.entries()[-1].setStyleSheet("""
                                                QLineEdit {
                                                background-color: qlineargradient(
                                                    x1:0, y1:0, x2:1, y2:1,
                                                    stop:0 #FDFEFF,
                                                    stop:0.3 #F5F9FF,
                                                    stop:0.8 #FAFCFE,
                                                    stop:1 #FFFFFF
                                                );
                                                color: #060270;
                                                border-radius: 5px;
                                                font-size: 17; font-weight: bold;
                                                margin-bottom: 7px;
                                                padding: 5px 10px 5px 5px;  /* Top, Right, Bottom, Left */
                                            }
                                            """)  # On aurait pu faire simple, mais amusons-nous un peu !!!
            pass

        def entries(self) -> list[QWidget]:
            return [self.age_entry, self.sexe_entry, self.output_entry]

        def labels(self) -> list[QLabel]:
            return [self.__label_age, self.__label_tip, self.__label_output]

        def __age_changed(self, age_str):
            try:
                age = int(age_str)
                sexe = self.sexe_entry.currentText()

                self.default_personne.age = age
                self.default_personne.sexe = sexe
                bareme = self.current_age_limite_table(personne=self.default_personne).bareme()
                self.output_entry.setText(f"{bareme}")
            except Exception as e:
                self.output_entry.setText("-")
                print(e)
                return
            pass

        def __sexe_changed(self, current_sexe):
            try:
                age = int(self.age_entry.text())
                sexe = current_sexe

                self.default_personne.age = age
                self.default_personne.sexe = sexe
                bareme = self.current_age_limite_table(personne=self.default_personne).bareme()
                self.output_entry.setText(f"{bareme}")
            except Exception as e:
                self.output_entry.setText("-")
                print(e)
                return

            pass

        def __age_limite_changed(self, current_age_limit):
            self.title.setText(f"Age limite du paiement de la rente : {current_age_limit} ans")
            # QLabel("Age limite du paiement de la rente : 100 ans")
            self.current_age_limite_table = self.__current_table(int(current_age_limit))

            age = self.age_entry.text()
            sexe = self.sexe_entry.currentText()

            self.__age_changed(age_str=age)
            self.__sexe_changed(current_sexe=sexe)
            pass

        #  -> TableTemporaire65 | TableTemporaire60 | TableTemporaire55 | TableTemporaire25 | TableTemporaire21

        def __current_table(self, age_limite: int):
            match age_limite:
                case 65:
                    return TableTemporaire65
                case 60:
                    return TableTemporaire60
                case 55:
                    return TableTemporaire55
                case 25:
                    return TableTemporaire25
                case 21:
                    return TableTemporaire21
            return None


class EnregistrerCalcul(QDialog):
    def __init__(self):
        super().__init__()
        self.entries = self.Entries()

        self.setWindowTitle("Enregistrement des données du calcul dans l'historique")
        icon = QIcon(QPixmap("assets/038-time.png"))
        self.setWindowIcon(icon)
        self.setModal(True)

        self.main_layout = QVBoxLayout(self)

        self.setStyleSheet("""
                                                    QWidget {
                                                        background-color: qlineargradient(
                                                                x1:0, y1:0, x2:1, y2:1,
                                                                stop:0 #B9D5F9,
                                                                stop:0.6 #e8f2ff,
                                                                stop:1 #d0e3ff
                                                            );
                                                    }

                                                    QLabel {
                                                        background-color: transparent;
                                                        color: #31588A;
                                                        margin-bottom: 3px;
                                                        font-size: 14px;
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

        lbl_num_contrat = QLabel("Entrer le numéro du contrat sinistré :")
        lbl_num_contrat.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(lbl_num_contrat)

        # L'entrée relative au numéro du contrat.
        self.main_layout.addWidget(self.entries.numero_contrat_entry)

        lbl_note_remarques = QLabel("Note ou remarques :")
        lbl_note_remarques.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(lbl_note_remarques)

        # L'entrée relative aux notes ou remarques.
        self.main_layout.addWidget(self.entries.note_remarques_entry)

        validate_button = QPushButton("Enregistrer")
        validate_button.setFixedSize(100, 30)
        validate_button.setStyleSheet("""
                                                        QPushButton {
                                                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                                stop:0 #2ea44f,       /* Vert GitHub vif */
                                                                stop:1 #2c974b);      /* Vert GitHub foncé */
                                                            border: 1px solid #2ea44f;
                                                            border-radius: 6px;
                                                            color: white;
                                                            font-weight: 600;
                                                            padding: 5px;
                                                            font-size: 12px;
                                                        }

                                                        QPushButton:hover {
                                                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                                stop:0 #34d058,       /* Vert GitHub clair (survol) */
                                                                stop:1 #2fbf4f);      /* Vert GitHub moyen */
                                                            border-color: #34d058;
                                                        }

                                                        QPushButton:pressed {
                                                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                                stop:0 #2c974b,       /* Vert foncé */
                                                                stop:1 #268740);      /* Vert très foncé */
                                                        }
                                                            """)
        self.main_layout.addWidget(validate_button)

        validate_button.clicked.connect(self.enregistrer_function)

    def enregistrer_function(self):
        choice = QMessageBox.question(None, "Valider ?", "Valdier l'enregistrement des calculs en l'état actuels ?")
        print(choice.Yes, choice.No, choice.name) # Oui = 16384, Non = 65536 # choice.name retourne "Yes" ou "No".
        if choice.name == "No":
            return
        print("Choice is Yes")

    class Entries:
        def __init__(self):
            self.numero_contrat_entry = QLineEdit()
            self.numero_contrat_entry.setMinimumWidth(400)
            self.numero_contrat_entry.setMaximumWidth(400)

            self.note_remarques_entry = QTextEdit()

            self.__set_style()

        def __set_style(self):
            self.numero_contrat_entry.setStyleSheet("""
                                                QLineEdit {
                                                background-color: qlineargradient(
                                                    x1:0, y1:0, x2:1, y2:1,
                                                    stop:0 #FDFEFF,
                                                    stop:0.3 #F5F9FF,
                                                    stop:0.8 #FAFCFE,
                                                    stop:1 #FFFFFF
                                                );
                                                color: #060270;
                                                border-radius: 5px;
                                                font-size: 17; font-weight: bold;
                                                margin-bottom: 7px;
                                                padding: 5px 10px 5px 5px;  /* Top, Right, Bottom, Left */
                                            }
                                            """)
            self.note_remarques_entry.setStyleSheet("""
                                                QTextEdit {
                                                background-color: qlineargradient(
                                                    x1:0, y1:0, x2:1, y2:1,
                                                    stop:0 #FDFEFF,
                                                    stop:0.3 #F5F9FF,
                                                    stop:0.8 #FAFCFE,
                                                    stop:1 #FFFFFF
                                                );
                                                color: #060270;
                                                border-radius: 5px;
                                                font-size: 17; font-weight: bold;
                                                margin-bottom: 7px;
                                                padding: 5px 10px 5px 5px;  /* Top, Right, Bottom, Left */
                                            }
                                            """)
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
main_layout.addWidget(EnregistrerCalcul())
main_window.show()

if __name__ == '__main__':
    sys.exit(app.exec())