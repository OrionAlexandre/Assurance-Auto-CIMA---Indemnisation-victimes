from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QStackedLayout, QStackedWidget, QVBoxLayout
import sys
from custom_widget import ButtonContainer, MenuButton

# Import des différentes pages
from calcul_indemnite import VictimeBlessee, VictimeDecedee, GestionGroupe
from valeur_point_ip import ValeurPoinIPWidget



class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
    pass


class MenuBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(269, 750)
        self.setStyleSheet("""background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #B9D5F9,
                stop:0.6 #e8f2ff,
                stop:1 #d0e3ff
            );
            border-radius: 8px;
            """)

        self.button_group = self.ButtonGroup()

        self.main_layout = QVBoxLayout(self)
        self._main_widget = QWidget(self)
        self.main_layout.addWidget(self._main_widget)

        # Le container du menu de l'application.
        self.main_widget_layout = QVBoxLayout(self._main_widget)

        # Le widget des indemnités.
        self.widget_one = ButtonContainer(intitule="  \u2B24 calcul des indemnités")
        self.main_widget_layout.addWidget(self.widget_one)

        for button in [self.button_group.but_victime_blessee,
                       self.button_group.but_victime_decedee,
                       self.button_group.but_groupe]:
            self.widget_one.main_layout.addWidget(button)

        # Le widget des tables.
        self.widget_two = ButtonContainer(intitule="  \u2B24 Tables des données CIMA")
        self.main_widget_layout.addWidget(self.widget_two)

        for button in [self.button_group.but_valeur_ip,
                       self.button_group.but_tabl_temporaires,
                       self.button_group.but_tabl_viagieres]:
            self.widget_two.main_layout.addWidget(button)

        # Les widgets des paramètres.
        self.widget_three = ButtonContainer(intitule="  \u2B24 Autres")
        self.main_widget_layout.addWidget(self.widget_three)

        for button in [self.button_group.but_historique,
                       self.button_group.but_methodes_calcul,
                       self.button_group.but_parametres]:
            self.widget_three.main_layout.addWidget(button)

    class ButtonGroup:
        def __init__(self):
            self.but_victime_blessee = MenuButton(text="Victime blessée", icon_path="assets/028-medical.png")
            self.but_victime_decedee = MenuButton(text="Victime décédée", icon_path="assets/021-user-1.png")
            self.but_groupe = MenuButton(text="Gestion par groupe", icon_path="assets/053-group.png")

            self.but_valeur_ip = MenuButton(text="Valeur du point d'IP", icon_path="assets/031-pulse.png")
            self.but_tabl_temporaires = MenuButton(text="Table de rentes temporaires", icon_path="assets/012-tabs.png")
            self.but_tabl_viagieres = MenuButton(text="Table de rentes permanentes", icon_path="assets/064-browsers.png")

            self.but_historique = MenuButton(text="Historique", icon_path="assets/038-time.png")
            self.but_methodes_calcul = MenuButton(text="Méthode de calcul", icon_path="assets/073-calculator.png")
            self.but_parametres = MenuButton(text="Paramètres", icon_path="assets/044-settings.png")
            pass
        pass
    pass


class StackPages(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1201, 750)

        # Instanciation et ajout des différentes pages.
        self.victime_blesse = VictimeBlessee()
        self.addWidget(self.victime_blesse)

        self.victime_decedee = VictimeDecedee()
        self.addWidget(self.victime_decedee)

        self.gestion_groupe = GestionGroupe()
        self.addWidget(self.gestion_groupe)

    # Implémentation des fonctions de gestions de pages.
    def show_victime_blessee(self):
        self.setCurrentWidget(self.victime_blesse)

    def show_victime_decedee(self):
        self.setCurrentWidget(self.victime_decedee)

    def show_gestion_groupe(self):
        self.setCurrentWidget(self.gestion_groupe)

    def show_vip_dialogue_widget(self):
        vip_dialogue_widget = ValeurPoinIPWidget()
        vip_dialogue_widget.show()
        vip_dialogue_widget.exec()
    pass


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assurance Auto - Indemnisation des victimes (Code CIMA)")
        icon = QIcon(QPixmap("assets/027-medical-1.png"))
        self.setWindowIcon(icon)

        self._main_container = QHBoxLayout(self)
        self.setFixedSize(1500, 770)

        self.setStyleSheet("""
                background-color: qlineargradient( \
                            x1:0, y1:0, x2:1, y2:1, \
                            stop:0 #FFFFFF,           /* Blanc pur */ \
                            stop:0.3 #F8FAFC,         /* Blanc froid GitHub */ \
                            stop:0.7 #F0F4F8,         /* Gris bleuté très pâle */ \
                            stop:1 #E8ECF0            /* Gris glacé GitHub */ \
                        );
        """)
        self.setContentsMargins(0, 0, 0, 0)

        # Ajout du menu de l'application.
        self.menu_bar = MenuBar()
        self._main_container.addWidget(self.menu_bar)

        # Ajout des différentes pages de l'application.
        self.pages = StackPages()
        self._main_container.addWidget(self.pages)

        # Rattachement des méthodes d'affichage.
        self.menu_bar.button_group.but_victime_blessee.clicked.connect(self.pages.show_victime_blessee)
        self.menu_bar.button_group.but_victime_decedee.clicked.connect(self.pages.show_victime_decedee)
        self.menu_bar.button_group.but_groupe.clicked.connect(self.pages.show_gestion_groupe)

        self.menu_bar.button_group.but_valeur_ip.clicked.connect(self.pages.show_vip_dialogue_widget)

    pass


if __name__ == '__main__':
    app = App()
    main_window = MainWindow()
    try:
        main_window.show()
    except Exception as e:
        print(e)
    sys.exit(app.exec())
