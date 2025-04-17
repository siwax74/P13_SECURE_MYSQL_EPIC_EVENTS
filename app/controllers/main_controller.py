import time
from app.controllers.client_controller import ClientController
from app.controllers.contract_controller import ContractController
from app.controllers.event_controller import EventController
from app.controllers.user_controller import UserController
from app.decorators import Decorator
from app.mixins import CRUDMixin
from app.views.main_view import MainView


class MainController(CRUDMixin):
    def __init__(self, session, authenticated_user, base_view):
        super().__init__(session)
        self.authenticated_user = authenticated_user
        self.base_view = base_view
        self.main_view = MainView(authenticated_user)
        self.user_controller = UserController(session, self.main_view, base_view)
        self.client_controller = ClientController(session, self.main_view, base_view)
        self.contract_controller = ContractController(session, self.main_view, base_view)
        self.event_controller = EventController(session, self.main_view, base_view)

    @Decorator.with_banner
    @Decorator.safe_execution
    def run(self):
        while True:
            choice = self.main_view.print_main_view()

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
                    break
            else:
                print("❌ Choix invalide. Veuillez réessayer.")
                return None

    def handle_logout(self):
        if self.base_view.print_logout_view() == "y":
            self.session.close()
            self.authenticated_user = None
            print("✅ Déconnecté avec succès.")
            return False
        return True
