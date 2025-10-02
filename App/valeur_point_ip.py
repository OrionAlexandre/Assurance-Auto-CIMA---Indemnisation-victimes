from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit

from algorithm.profils import Personne
from algorithm.tables import SituationMatrimoniale, ValeurPointIP


class ValeurPoinIPWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Valeur du point d'IP")
        icon = QIcon(QPixmap("assets/031-pulse.png"))
        self.setWindowIcon(icon)
        self.setModal(True)

        self.entries = self.Entries()

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
        label_ = QLabel("Valeur du poind d'IP")
        label_.setStyleSheet("""
                                            QLabel {
                                                color: #34495e;
                                                font-size: 16px;
                                                font-weight: bold;
                                                padding-bottom: 8px;
                                                border-bottom: 2px solid #3498db;  /* Ligne de séparation bleue */
                                                margin-bottom: 7px;
                                            }
                                        """)
        label_.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(label_)

        # Le widget des entrées.
        self.__entries_widget = QWidget()
        self.__entries_layout = QGridLayout(self.__entries_widget)
        self.__entries_widget.setStyleSheet("""
                background-color: transparent;
                border-radius: 7px;
                border: 3px;
                border-color: blue;
        """)
        self.main_layout.addWidget(self.__entries_widget)

        row, col = 0, 0
        for label in self.entries.labels():
            self.__entries_layout.addWidget(label, row, col)
            col += 1

        row, col = 1, 0
        for entry in self.entries.entries():
            self.__entries_layout.addWidget(entry, row, col)
            col += 1


    class Entries:
        def __init__(self):
            self.age_entry = QLineEdit()
            self.taux_ip_entry = QLineEdit()
            self.output_entry = QLineEdit()

            self.__label_age = QLabel("L'âge de la victime :")
            self.__label_tip = QLabel("Taux d'IP la victime (0-100) :")
            self.__label_output = QLabel("Valeur du point d'IP :")

            self.output_entry.setReadOnly(True) # Pour empêcher les modifications de l'utilisateur.

            self.age_entry.setText(f"{0}")
            self.taux_ip_entry.setText(f"{0.0}")
            self.output_entry.setText(f"{0}")

            self.age_entry.textChanged.connect(self.age_changed)
            self.taux_ip_entry.textChanged.connect(self.taux_ip_changed)

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
            taux_ip: float = 0.0

            self.__set_style()

        def __set_style(self):
            for entry in self.entries()[0:2]:
                entry.setStyleSheet("""
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
                                font-size: 15; font-weight: bold;
                                margin-bottom: 7px;
                                padding: 5px 10px 5px 5px;  /* Top, Right, Bottom, Left */
                            }
                            """) # On aurait pu faire simple, mais amusons-nous un peu !!!
            pass

        def entries(self) -> list[QLineEdit]:
            return [self.age_entry, self.taux_ip_entry, self.output_entry]

        def labels(self) -> list[QLabel]:
            return [self.__label_age, self.__label_tip, self.__label_output]

        def age_changed(self, age_str: str):
            try:
                age = int(age_str)
                self.default_personne.age = age

                taux_ip = float(self.taux_ip_entry.text())

                if int(taux_ip) == 0:
                    self.output_entry.setText(f"{0}")
                    return

                valeur_ip = ValeurPointIP(person=self.default_personne, taux_ip=taux_ip)

                self.output_entry.setText(f"{valeur_ip.valeur}")
            except:
                self.output_entry.setText("-")
                return

        def taux_ip_changed(self, taux_ip_str: str):
            try:
                taux_ip = float(taux_ip_str)

                if int(taux_ip) == 0:
                    self.output_entry.setText(f"{0}")
                    return

                age = float(self.age_entry.text())
                self.default_personne.age = int(age)

                valeur_ip = ValeurPointIP(person=self.default_personne, taux_ip=taux_ip)

                self.output_entry.setText(f"{valeur_ip.valeur}")
            except:
                self.output_entry.setText("-")
                return
    pass

