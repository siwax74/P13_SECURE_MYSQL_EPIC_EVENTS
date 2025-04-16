from app.decorators import safe_execution
from app.mixins import CRUDMixin
from app.models.client import Client
from app.models.user import User
from app.permissions import BasePermissions
from app.views.client_view import ClientView
from app.decorators import with_banner


#######################################################################################################################
#                                                    CLIENTS                                                          #
#######################################################################################################################
class ClientController(CRUDMixin):
    def __init__(self, session, main_view):
        super().__init__(session)
        self.main_view = main_view
        self.client_view = ClientView(main_view)
        self.authenticated_user = main_view.authenticated_user

    @with_banner
    def handle_client_menu(self):
        while True:
            choice = self.client_view.print_client_menu()

            actions = {
                "1": self.list_clients,
                "2": self.create_client,
                "3": self.update_client,
                "4": self.delete_client,
                "5": "exit",
            }

            action = actions.get(choice)
            if action == "exit":
                break
            elif action:
                action()
            else:
                print("❌ Choix invalide.")

    @with_banner
    @safe_execution
    @BasePermissions.check_permission("is_commercial")
    def create_client(self):
        name, email, phone, company = self.client_view.print_create_client_view()
        if not all([name, email, phone, company]):
            raise ValueError("❌ Tous les champs sont obligatoires.")

        contact_commercial = self.session.query(User).filter_by(is_commercial=True).first()
        if not contact_commercial:
            raise ValueError("❌ Aucun commercial disponible.")
        self.create(
            Client, name=name, email=email, phone=phone, company=company, contact_commercial=contact_commercial
        )

    @with_banner
    @safe_execution
    @BasePermissions.check_permission("is_commercial")
    def update_client(self):
        clients = self.list(Client)
        client_id = self.client_view.print_update_client_view(clients)

        client = self.session.get(Client, client_id)
        if not client:
            raise ValueError("❌ Client introuvable.")

        name, email, phone, company = self.client_view.print_update_client_form()
        if name:
            self.update(Client, client_id, name=name)
        if email:
            self.update(Client, client_id, email=email)
        if phone:
            self.update(Client, client_id, phone=phone)
        if company:
            self.update(Client, client_id, company=company)

    @with_banner
    @safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_client(self):
        clients = self.list(Client)
        client_id = self.client_view.print_delete_client_view(clients)

        client = self.session.get(Client, client_id)
        if not client:
            raise ValueError("❌ Client introuvable.")

        self.delete(Client, client_id)

    @with_banner
    @safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def list_clients(self):
        clients = self.list(Client)
        self.cli_view.print_banner()
        self.client_view.print_clients_list_view(clients)
