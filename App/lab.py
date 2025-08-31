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

class RecapitulatifVictimeBlessee(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Etat récapitulatif")

        self.output_data = self.OutputData()

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
        self.main_layout = QVBoxLayout(self)

        entete_label = QLabel("Etat récapitulatif")
        entete_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        entete_label.setStyleSheet("background: transparent; font-weight: bold; font-size: 17px;")
        self.main_layout.addWidget(entete_label)

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        # self.__separator.setFixedWidth(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.main_layout.addWidget(self.__separator)

        self.main_layout.addWidget(QLabel("Cumul des frais médicaux et des honoraires d'expert :"))
        self.main_layout.addWidget(self.output_data.cumul_frais_medicaux_honoraires)
        self.main_layout.addWidget(QLabel("Indemnité au titre de l'incapacité temporaire :"))
        self.main_layout.addWidget(self.output_data.indemnite_it)
        self.main_layout.addWidget(QLabel("Indemnité au titre de l'incapacité permanente :"))
        self.main_layout.addWidget(self.output_data.indemnite_ip)

        self.main_layout.addWidget(QLabel("Indemnité au titre du besoin d'assistance d'une tierce personne\n(taux d'ip >= 80%) :"))
        self.main_layout.addWidget(self.output_data.assistance_tp)
        self.main_layout.addWidget(QLabel("Indemnité au titre du prétium doloris :"))
        self.main_layout.addWidget(self.output_data.pretium_doloris)
        self.main_layout.addWidget(QLabel("Indemnité au titre du préjudice esthétique :"))
        self.main_layout.addWidget(self.output_data.prejudice_esthetique)

        self.main_layout.addWidget(QLabel("Perte de gains professionnel futur :"))
        self.main_layout.addWidget(self.output_data.perte_gain_professionnel)
        self.main_layout.addWidget(QLabel("Indemnité au titre du préjudice scolaire :"))
        self.main_layout.addWidget(self.output_data.prejudice_scolaire)
        self.main_layout.addWidget(QLabel("Indemnité au titre du préjudice moral du conjoint\n(taux d'ip = 100% et au moins conjoint) :"))
        self.main_layout.addWidget(self.output_data.prejudice_moral_conjoint)

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        # self.__separator.setFixedWidth(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.main_layout.addWidget(self.__separator)

        label_total = QLabel("Total à provisions :")
        label_total.setStyleSheet("font-weight: bold; margin-bottom: 3px;")
        self.main_layout.addWidget(label_total)
        self.main_layout.addWidget(self.output_data.total)

    class OutputData:
        def __init__(self):

            self.cumul_frais_medicaux_honoraires = QLabel(f"{0} F CFA")
            self.indemnite_it = QLabel(f"{0} F CFA")
            self.indemnite_ip = QLabel(f"{0} F CFA")
            self.assistance_tp = QLabel(f"{0} F CFA")
            self.pretium_doloris = QLabel(f"{0} F CFA")
            self.prejudice_esthetique = QLabel(f"{0} F CFA")
            self.perte_gain_professionnel = QLabel(f"{0} F CFA")
            self.prejudice_scolaire = QLabel(f"{0} F CFA")
            self.prejudice_moral_conjoint = QLabel(f"{0} F CFA")
            self.total = QLabel(f"{0} F CFA")

            self.total.setStyleSheet("font-weight: bold; margin-bottom: 3px; color: green; font-size: 14px; margin-left: 12px;")

            for label in [self.cumul_frais_medicaux_honoraires,
                          self.indemnite_it,
                          self.indemnite_ip,
                          self.assistance_tp,
                          self.pretium_doloris,
                          self.prejudice_esthetique,
                          self.perte_gain_professionnel,
                          self.prejudice_scolaire,
                          self.prejudice_moral_conjoint]:
                label.setStyleSheet("""
                                                QLabel {
                                                    background-color: transparent;
                                                    color: #31588A;
                                                    margin-bottom: 3px;
                                                    margin-left: 12px;
                                                    font-size: 14px;
                                                    font-weight: bold;
                                                    margin-bottom: 7px;
                                                }""")
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
main_layout.addWidget(RecapitulatifVictimeBlessee())
main_window.show()

if __name__ == '__main__':
    sys.exit(app.exec())