from app.mixins import CRUDMixin
from app.models.client import Client
from app.models.user import User
from app.permissions import BasePermissions
from app.views.client_view import ClientView
from app.decorators import Decorator
from app.regex import is_valid_company, is_valid_email, is_valid_name, is_valid_phone


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

    ############################################### MENU CLIENT #######################################################
    @Decorator.with_banner
    @BasePermissions.check_permission("is_commercial", "is_management")
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

    ############################################### CREATE CLIENT #####################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial")
    def create_client(self):
        name, email, phone, company = self.client_view.print_create_client_view()

        if not name or not is_valid_name(name):
            print("❌ Le champ 'Nom' est obligatoire.")
            return None
        if not email or not is_valid_email(email):
            print("❌ Le champ 'Email' est obligatoire.")
            return None
        if not phone or not is_valid_phone(phone):
            print("❌ Le champ 'Téléphone' est obligatoire.")
            return None
        if not company or not is_valid_company(company):
            print("❌ Le champ 'Entreprise' est obligatoire.")
            return None

        contact_commercial = self.authenticated_user
        if not contact_commercial or not contact_commercial.is_commercial:
            print("❌ Seul un commercial peut créer un client.")
            return None

        return self.create(
            Client, name=name, email=email, phone=phone, company=company, contact_commercial=contact_commercial
        )

    ############################################### UPDATE CLIENT #####################################################
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
        if client.contact_commercial_id != self.authenticated_user.id:
            print("❌ Vous ne pouvez modifier que vos propres clients.")
            return None

        name, email, phone, company = self.client_view.print_update_client_form()

        update_data = {}
        if is_valid_name(name):
            update_data["name"] = name
        if is_valid_email(email):
            update_data["email"] = email
        if is_valid_phone(phone):
            update_data["phone"] = phone
        if is_valid_company(company):
            update_data["company"] = company

        if update_data:
            self.update(Client, client_id, **update_data)
        else:
            print("⚠️ Aucun champ à mettre à jour.")
        return None

    ############################################### DELETE CLIENT #####################################################
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

    ############################################### LIST CLIENTS ######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def list_clients(self):
        clients = self.list(Client)
        if not clients:
            print("❌ Aucun client trouvé.")
            return None
        return self.client_view.print_clients_list_view(clients)
