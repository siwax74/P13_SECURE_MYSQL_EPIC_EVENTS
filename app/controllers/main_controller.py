import time
from typing import Optional
from app.controllers.client_controller import ClientController
from app.controllers.contract_controller import ContractController
from app.controllers.event_controller import EventController
from app.controllers.user_controller import UserController
from app.decorators import Decorator
from app.mixins import CRUDMixin
from app.views.BaseView import BaseView
from app.views.main_view import MainView


#######################################################################################################################
#                                                    MAIN CONTROLLER                                                  #
#######################################################################################################################


class MainController(CRUDMixin):
    """
    Contrôleur principal gérant les menus et l'accès aux autres contrôleurs (client, contrat, événement, utilisateur).
    """

    def __init__(self, session, authenticated_user, base_view) -> None:
        """
        Initialise le contrôleur principal.

        Args:
            session (Session): Session SQLAlchemy pour les requêtes à la base de données.
            authenticated_user (User): L'utilisateur actuellement authentifié.
            base_view (BaseView): Vue de base utilisée pour l'affichage.
        """
        super().__init__(session)
        self.authenticated_user = authenticated_user
        self.base_view = base_view
        self.main_view = MainView(authenticated_user)
        self.user_controller = UserController(session, self.main_view, base_view)
        self.client_controller = ClientController(session, self.main_view, base_view)
        self.contract_controller = ContractController(session, self.main_view, base_view)
        self.event_controller = EventController(session, self.main_view, base_view)

    ############################################### MENU MAIN #########################################################
    @Decorator.safe_execution
    def run(self) -> Optional[bool]:
        """
        Démarre la boucle du menu principal. Permet à l'utilisateur de naviguer entre les différentes sections.
        Si l'utilisateur choisit de se déconnecter, cela arrête la boucle.

        Returns:
            Optional[bool]: Si False est retourné, la boucle principale est arrêtée (déconnexion).
        """
        while True:
            self.base_view.print_banner()
            choice: str = self.main_view.print_main_view()

            menu_actions = {
                "1": self.contract_controller.handle_contract_menu,
                "2": self.client_controller.handle_client_menu,
                "3": self.event_controller.handle_event_menu,
                "4": self.user_controller.handle_user_menu,
                "5": self.handle_logout,
            }

            action = menu_actions.get(choice)
            if action:
                should_continue = action()
                if should_continue is False:
                    return False
            else:
                print("❌ Choix invalide. Veuillez réessayer.")
                return None

    ############################################### LOGOUT ###########################################################
    def handle_logout(self) -> bool:
        """
        Gère la déconnexion de l'utilisateur. Ferme la session et met à jour l'état de l'utilisateur.

        Returns:
            bool: Retourne False si l'utilisateur souhaite se déconnecter, sinon True pour rester connecté.
        """
        if self.base_view.print_logout_view() == "y":
            self.session.close()
            self.authenticated_user = None
            print("✅ Déconnecté avec succès.")
            return False
        return True
