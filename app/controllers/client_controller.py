from app.mixins import CRUDMixin
from app.models.client import Client
from app.models.user import User
from app.permissions import BasePermissions
from app.views.client_view import ClientView
from app.decorators import Decorator
from app.regex import is_valid_company, is_valid_email, is_valid_name, is_valid_phone
from typing import Optional, Any
from sqlalchemy.orm import Session


#######################################################################################################################
#                                                    CLIENTS                                                          #
#######################################################################################################################
class ClientController(CRUDMixin):
    def __init__(self, session: Session, main_view: Any, base_view: Any) -> None:
        """
        Initialise le contrôleur de client avec la session, la vue principale et la vue de base.
        """
        super().__init__(session)
        self.base_view = base_view
        self.main_view = main_view
        self.client_view = ClientView(main_view)
        self.authenticated_user = main_view.authenticated_user

    @Decorator.with_banner
    @BasePermissions.check_permission("is_commercial", "is_management")
    def handle_client_menu(self) -> None:
        """
        Gère le menu principal des clients avec différentes options (lister, créer, modifier, supprimer).
        Accessible uniquement aux utilisateurs commerciaux ou managers.
        """
        while True:
            choice: str = self.client_view.print_client_menu()

            actions: dict[str, Optional[Any]] = {
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
    def create_client(self) -> Optional[Client]:
        """
        Crée un nouveau client à partir des informations saisies par l'utilisateur.
        Vérifie les permissions, la validité des champs, et assigne le commercial courant comme contact.
        """
        name: str
        email: str
        phone: str
        company: str
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

        contact_commercial: Optional[User] = self.authenticated_user
        if not contact_commercial or not contact_commercial.is_commercial:
            print("❌ Seul un commercial peut créer un client.")
            return None

        return self.create(
            Client,
            name=name,
            email=email,
            phone=phone,
            company=company,
            contact_commercial=contact_commercial,
        )

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial")
    def update_client(self) -> Optional[None]:
        """
        Met à jour les informations d’un client existant appartenant au commercial authentifié.
        Affiche un formulaire, vérifie les droits, et applique les changements validés.
        """
        clients: list[Client] = self.list(Client)
        client_id: int = self.client_view.print_update_client_view(clients)

        client: Optional[Client] = self.session.get(Client, client_id)
        if not client:
            print("❌ Client introuvable.")
            return None
        if client.contact_commercial_id != self.authenticated_user.id:
            print("❌ Vous ne pouvez modifier que vos propres clients.")
            return None

        name, email, phone, company = self.client_view.print_update_client_form()

        update_data: dict[str, Any] = {}
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

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_client(self) -> Optional[None]:
        """
        Supprime un client de la base de données après sélection.
        Seuls les utilisateurs ayant les droits de management peuvent effectuer cette opération.
        """
        clients: list[Client] = self.list(Client)
        client_id: int = self.client_view.print_delete_client_view(clients)

        client: Optional[Client] = self.session.get(Client, client_id)
        if not client:
            print("❌ Client introuvable.")
            return None

        return self.delete(Client, client_id)

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def list_clients(self) -> Optional[None]:
        """
        Affiche la liste des clients existants.
        Disponible pour tous les rôles autorisés : commerciaux, support et management.
        """
        clients: list[Client] = self.list(Client)
        if not clients:
            print("❌ Aucun client trouvé.")
            return None
        return self.client_view.print_clients_list_view(clients)
