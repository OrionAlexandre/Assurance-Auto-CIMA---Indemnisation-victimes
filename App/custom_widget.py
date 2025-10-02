from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QGridLayout, \
    QMessageBox, QListWidget
from PyQt6.QtGui import QIcon

from database_manager import personnes, rechercher_personne_par_id
from algorithm.profils import Enfant, Conjoint, Ascendant, Collateral, Personne

scroll_style = """
        /* Style de la barre de défilement horizontale */
        QScrollBar:horizontal {
            height: 10px;
            background: transparent;
            border: none;
            margin: 0px;
        }

        /* Arrière-plan pointillé */
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: transparent;
        }

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
            height: 0px;
        }

        /* Curseur principal avec dégradé bleu */
        QScrollBar::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #1E3A8A, stop:0.5 #2563EB, stop:1 #1E3A8A);
            min-width: 40px;
            border-radius: 3px;
            margin: 0px 10px;  /* Espace pour les extrémités */
        }

        /* Effet de survol */
        QScrollBar::handle:horizontal:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #1E40AF, stop:0.5 #3B82F6, stop:1 #1E40AF);
        }

        /* Effet lors du clic */
        QScrollBar::handle:horizontal:pressed {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #1E3A8A, stop:0.5 #1D4ED8, stop:1 #1E3A8A);
        }

        /* Style des extrémités (flèches stylisées) */
        QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
            width: 6px;
            height: 10px;
            background: #2563EB;
        }

        QScrollBar::left-arrow:horizontal {
            subcontrol-origin: margin;
            subcontrol-position: left;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }

        QScrollBar::right-arrow:horizontal {
            subcontrol-origin: margin;
            subcontrol-position: right;
            border-top-left-radius: 3px;
            border-bottom-left-radius: 3px;
        }
        """

class MenuButton(QPushButton):
    def __init__(self, icon_path: str, text: str = "Menu button"):
        super().__init__(text=text)
        icon = QIcon(icon_path)
        self.setIcon(icon)
        self.setIconSize(QSize(30, 30))

        self.setStyleSheet("""
                QPushButton {
                    color: #6F809C;
                    padding: 6px 14px;
                    text-align: left;
                    font-size: 12px;
                }
                QPushButton::icon {
                    padding-right: 8px;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        x1: 0, y1: 0,
                        x2: 1, y2: 1,  /* Diagonale ↘ */
                        stop: 0 #86B3FA,
                        stop: 0.7 #B1D6FA,
                        stop: 1 #97BBFA
                    );
                }
                QPushButton:pressed {
                    background: qlineargradient(
                        x1: 0, y1: 0,
                        x2: 1, y2: 1,  /* Diagonale ↘ */
                        stop: 0 #62A7FA,
                        stop: 0.7 #5C9DEB,
                        stop: 1 #5089CC
                    );
                    color: #DFE0E6;
                }
                """)
    pass


class ButtonContainer(QWidget):
    def __init__(self, intitule: str = "Widget des bouttons"):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        self.__trait = QWidget()
        self.__trait.setFixedHeight(1)
        self.__trait.setStyleSheet("background-color: #31588A; margin: 6px 0px; margin-top: 7px;")
        self.main_layout.addWidget(self.__trait)

        self.__label = QLabel(intitule)
        self.__label.setStyleSheet("""
                    color: #8397B8;
                    margin-left: 3px;
                    font-weight: bold;
                """)
        self.main_layout.addWidget(self.__label)

    pass


class CustomLabelName(QLabel):
    def __init__(self, text: str):
        super().__init__(text=text)

        self.setStyleSheet("""
                            color: #DFE3ED;
                            font-size: 10pt;
                            margin-bottom: 0px;
                            """)


class ProfilLabel(QLabel):
    def __init__(self, text: str):
        super().__init__(text=text)

        self.setStyleSheet("""
                        font-size: 12pt;
                        font-weight: bold;
                        margin-bottom: 12px;
                            """)


class CustomCalculusQWidget(QWidget):
    def __init__(self, intitule: str = "Widget personnalisé"):
        super().__init__()

        # Configuration de base du widget
        self.setFixedSize(350, 400)
        self.setContentsMargins(5, 5, 5, 5)  # Marge interne

        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(5)  # Espacement entre les éléments

        # Configuration du titre
        self.title = QLabel(intitule)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #31588A;
                margin-bottom: 3px;
                font-size: 14px;
            }
        """)

        # Barre de séparation
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        self.__separator.setStyleSheet("background-color: #060270")

        # Zone de contenu (pour les classes enfants)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Ajout des éléments au layout principal
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.__separator)
        self.main_layout.addWidget(self.content_widget, 1)  # Le facteur 1 permet l'expansion

        # Style du widget principal
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
            QLabel {
                color: #060270;
                font-size: 12;
                margin-bottom: 1px;
                margin-top: 3px;
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
                margin-bottom: 12px;
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

    def add_content(self, widget: QWidget):
        """Méthode pour ajouter du contenu dans la zone principale"""
        self.content_layout.addWidget(widget)


class ScrollableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration principale
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Création de la scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(False)  # IMPORTANT : Doit être False
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Appliquez le style à votre scroll area
        self.scroll.setStyleSheet(scroll_style)

        # Widget conteneur (doit être plus large que la scroll area)
        self.container = QWidget()
        self.container.setMinimumWidth(4100)
        self.container.setMinimumHeight(self.height())

        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(20)

        # Configuration finale
        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)

        # Style
        self.container.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #B9D5F9,
                stop:0.6 #e8f2ff,
                stop:1 #d0e3ff);
            border-radius: 8px;
        """)


class WidgetContainer(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(widget)


class RepartitionWidget(QWidget):
    def __init__(self, intitule: str, height: int, list_ayants_droit: list[Enfant] | list[Conjoint] | list[Ascendant] | list[Collateral], prejudice_economique: bool = True):
        super().__init__()
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

        self.setMaximumHeight(30 * height + 150)

        self.prejudice_economique = prejudice_economique
        self.list_ayant_droit = list_ayants_droit
        self.height = height

        self.main_layout = QGridLayout(self)

        label_intitule = QLabel(intitule)
        label_intitule.setStyleSheet("font-weight: bold; margin-bottom: 3px;")
        label_intitule.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(label_intitule, 0, 0, 1, 4) if prejudice_economique else self.main_layout.addWidget(label_intitule, 0, 0, 1, 3)

        label_noms = QLabel("Noms :")
        label_prenoms = QLabel("Prénoms :")
        label_pj_eco = QLabel("Préjudices économiques :")
        label_pj_mora = QLabel("Préjudices moraux :")

        labels_list = [label_noms, label_prenoms, label_pj_eco, label_pj_mora] if prejudice_economique else [label_noms, label_prenoms, label_pj_mora]

        col = 0
        for label in labels_list:
            label.setStyleSheet("font-weight: bold; margin-right: 12px;")
            # label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.main_layout.addWidget(label, 1, col)
            col += 1

        # On ajoute les résultats.
        self.add_informations(self.list_ayant_droit)


    def add_informations(self, list_ayants_droit: list[Enfant] | list[Conjoint] | list[Ascendant] | list[Collateral]):
        row, col = 2, 0

        if not list_ayants_droit:
            for _ in range(self.height):
                # Barre de séparation.
                self.__separator = QWidget()
                self.__separator.setFixedHeight(1)
                # self.__separator.setFixedWidth(1)
                self.__separator.setStyleSheet("background-color: #060270")
                self.main_layout.addWidget(self.__separator, row, col, 1, 4)
                row += 1

                self.main_layout.addWidget(QLabel("-"), row, 0)
                self.main_layout.addWidget(QLabel("-"), row, 1)
                self.main_layout.addWidget(QLabel("-"), row, 2)
                self.main_layout.addWidget(QLabel("-"), row, 3)
                row += 1

            # Barre de séparation.
            self.__separator = QWidget()
            self.__separator.setFixedHeight(1)
            # self.__separator.setFixedWidth(1)
            self.__separator.setStyleSheet("background-color: #060270")
            self.main_layout.addWidget(self.__separator, row, col, 1, 4)

            row += 1
            label_total = QLabel("Total :")
            label_sum_prejudice_eco = QLabel(f"{0.00} F CFA")
            label_sum_prejudice_moral = QLabel(f"{0.00} F CFA")

            label_total.setStyleSheet("font-weight: bold; margin-bottom: 3px;")
            label_sum_prejudice_eco.setStyleSheet("font-weight: bold; margin-bottom: 3px; color: green;")
            label_sum_prejudice_moral.setStyleSheet("font-weight: bold; margin-bottom: 3px; color: green;")

            self.main_layout.addWidget(label_total, row, 0, 1, 2)
            self.main_layout.addWidget(label_sum_prejudice_eco, row, 2)
            self.main_layout.addWidget(label_sum_prejudice_moral, row, 3)

            row += 1
            # Barre de séparation (La dernière barre).
            self.__separator = QWidget()
            self.__separator.setFixedHeight(1)
            # self.__separator.setFixedWidth(1)
            self.__separator.setStyleSheet("background-color: #060270")
            self.main_layout.addWidget(self.__separator, row, col, 1, 4)
            return

        for individu in list_ayants_droit:
            # Barre de séparation.
            self.__separator = QWidget()
            self.__separator.setFixedHeight(1)
            self.__separator.setStyleSheet("background-color: #060270")
            self.main_layout.addWidget(self.__separator, row, col, 1, 4)
            row += 1

            self.main_layout.addWidget(QLabel(f"{individu.nom}"), row, col)
            col += 1
            self.main_layout.addWidget(QLabel(f"{individu.prenom}"), row, col)
            col += 1
            self.main_layout.addWidget(QLabel(f"{self.format_nombre_fr(individu.prejudice_economique)} F CFA"), row, col)
            col += 1
            self.main_layout.addWidget(QLabel(f"{self.format_nombre_fr(individu.prejudice_moral)} F CFA"), row, col)

            row += 1
            col = 0


        if len(list_ayants_droit) < self.height:
            for _ in range(self.height - len(list_ayants_droit)):
                # Barre de séparation.
                self.__separator = QWidget()
                self.__separator.setFixedHeight(1)
                # self.__separator.setFixedWidth(1)
                self.__separator.setStyleSheet("background-color: #060270")
                self.main_layout.addWidget(self.__separator, row, col, 1, 4)
                row += 1

                self.main_layout.addWidget(QLabel("-"), row, 0)
                self.main_layout.addWidget(QLabel("-"), row, 1)
                self.main_layout.addWidget(QLabel("-"), row, 2)
                self.main_layout.addWidget(QLabel("-"), row, 3)
                row += 1

        # Barre de séparation.
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        # self.__separator.setFixedWidth(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.main_layout.addWidget(self.__separator, row, col, 1, 4)

        sum_preju_eco = sum([individu.prejudice_economique for individu in list_ayants_droit])
        sum_preju_moral = sum([individu.prejudice_moral for individu in list_ayants_droit])

        row += 1
        label_total = QLabel("Total :")
        label_sum_prejudice_eco = QLabel(f"{self.format_nombre_fr(sum_preju_eco)} F CFA")
        label_sum_prejudice_moral = QLabel(f"{self.format_nombre_fr(sum_preju_moral)} F CFA")

        label_total.setStyleSheet("font-weight: bold; margin-bottom: 3px;")
        label_sum_prejudice_eco.setStyleSheet("font-weight: bold; margin-bottom: 3px; color: green;")
        label_sum_prejudice_moral.setStyleSheet("font-weight: bold; margin-bottom: 3px; color: green;")

        self.main_layout.addWidget(label_total, row, 0, 1, 2)
        self.main_layout.addWidget(label_sum_prejudice_eco, row, 2)
        self.main_layout.addWidget(label_sum_prejudice_moral, row, 3)

        row += 1
        # Barre de séparation (La dernière barre).
        self.__separator = QWidget()
        self.__separator.setFixedHeight(1)
        # self.__separator.setFixedWidth(1)
        self.__separator.setStyleSheet("background-color: #060270")
        self.main_layout.addWidget(self.__separator, row, col, 1, 4)

    def format_nombre_fr(self, nombre, decimales=2):
        """
        Formate un nombre selon les conventions françaises
        :param nombre: Nombre à formater (int, float ou str numérique)
        :param decimales: Nombre de décimales à afficher
        :return: Chaîne formatée
        """
        # Gestion des types et conversion
        if isinstance(nombre, str):
            try:
                nombre = float(nombre) if '.' in nombre else int(nombre)
            except ValueError:
                return nombre  # Retourne la chaîne originale si conversion impossible

        # Séparation partie entière/décimale
        if isinstance(nombre, int):
            partie_entiere = str(abs(nombre))
            partie_decimale = ''
        else:
            partie_entiere, partie_decimale = f"{abs(nombre):.{decimales}f}".split('.')

        # Ajout des espaces comme séparateurs de milliers
        partie_entiere_formatee = []
        longueur = len(partie_entiere)

        for i, chiffre in enumerate(partie_entiere, 1):
            partie_entiere_formatee.append(chiffre)
            if (longueur - i) % 3 == 0 and i != longueur:
                partie_entiere_formatee.append(' ')

        # Assemblage final
        signe = '-' if nombre < 0 else ''
        nombre_formate = signe + ''.join(partie_entiere_formatee)

        if partie_decimale:
            nombre_formate += ',' + partie_decimale

        return nombre_formate


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
            self.addItem(f"{personne.id} - {personne.nom} - {personne.prenom} - Sexe : {personne.sexe}")

        self.personne = rechercher_personne_par_id(1)  # Par défaut la première personne.

    def __clear_all(self):
        self.clear()
        pass

    def reload_content(self):
        self.__clear_all()

        self.liste_personnes = personnes()

        for personne in self.liste_personnes:
            self.addItem(f"{personne.id} - {personne.nom} - {personne.prenom} - Sexe : {personne.sexe}")

        self.personne = rechercher_personne_par_id(1)  # Par défaut la première personne.

        print("Liste rechargée complètement !!!")
        pass

    pass


class ListEnfants(CustomAyantsDroitsList):
    def __init__(self, personne: Personne):
        self.personne = personne
        super().__init__()

        if self.personne is not None:
            self.loader = LoadList(list_view_widget=self, list_to_load=self.personne.enfants)
            return
    pass


class ListConjoints(CustomAyantsDroitsList):
    def __init__(self, personne: Personne):
        self.personne = personne
        super().__init__()

        if self.personne is not None:
            self.loader = LoadList(list_view_widget=self, list_to_load=self.personne.conjoints)
            return

    pass


class ListCollateraux(CustomAyantsDroitsList):
    def __init__(self, personne: Personne):
        self.personne = personne
        super().__init__()

        if self.personne is not None:
            self.loader = LoadList(list_view_widget=self, list_to_load=self.personne.collateraux)
            return

    pass


class ListAscendants(CustomAyantsDroitsList):
    def __init__(self, personne: Personne):
        self.personne = personne
        super().__init__()

        if self.personne is not None:
            self.loader = LoadList(list_view_widget=self, list_to_load=self.personne.ascendants)
            return

    pass



