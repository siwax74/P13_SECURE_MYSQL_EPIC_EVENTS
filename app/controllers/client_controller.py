from app.mixins import CRUDMixin
from app.models.client import Client
from app.models.user import User
from app.permissions import BasePermissions
from app.views.client_view import ClientView
from app.decorators import Decorator


#######################################################################################################################
#                                                    CLIENTS                                                          #
#######################################################################################################################
class ClientController(CRUDMixin):
    def __init__(self, session, main_view, base_view):
        super().__init__(session)
        self.base_view = base_view
        self.main_view = main_view
        self.client_view = ClientView(main_view)
        self.authenticated_user = main_view.authenticated_user

    @Decorator.with_banner
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
                return None

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial")
    def create_client(self):
        name, email, phone, company = self.client_view.print_create_client_view()

        # Check each argument individually
        if not name:
            print("❌ Le champ 'Nom' est obligatoire.")
            return None
        if not email:
            print("❌ Le champ 'Email' est obligatoire.")
            return None
        if not phone:
            print("❌ Le champ 'Téléphone' est obligatoire.")
            return None
        if not company:
            print("❌ Le champ 'Entreprise' est obligatoire.")
            return None

        contact_commercial = self.session.query(User).filter_by(is_commercial=True).first()
        if not contact_commercial:
            print("❌ Aucun commercial disponible.")
            return None

        return self.create(
            Client, name=name, email=email, phone=phone, company=company, contact_commercial=contact_commercial
        )

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial")
    def update_client(self):
        clients = self.list(Client)
        client_id = self.client_view.print_update_client_view(clients)

        client = self.session.get(Client, client_id)
        if not client:
            print("❌ Client introuvable.")
            return None

        name, email, phone, company = self.client_view.print_update_client_form()
        if not name:
            return None
        else:
            self.update(Client, client_id, name=name)
        if not email:
            return None
        else:
            self.update(Client, client_id, email=email)
        if not phone:
            return None
        else:
            self.update(Client, client_id, phone=phone)
        if not company:
            return None
        else:
            self.update(Client, client_id, company=company)

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_client(self):
        clients = self.list(Client)
        client_id = self.client_view.print_delete_client_view(clients)

        client = self.session.get(Client, client_id)
        if not client:
            print("❌ Client introuvable.")
            return None

        return self.delete(Client, client_id)

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def list_clients(self):
        clients = self.list(Client)
        if not clients:
            print("❌ Aucun client trouvé.")
            return None
        return self.client_view.print_clients_list_view(clients)
