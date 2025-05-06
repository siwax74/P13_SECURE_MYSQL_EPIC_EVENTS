import re
from typing import Any, Optional
from app.mixins import CRUDMixin
from app.decorators import Decorator
from app.models.client import Client
from app.models.contract import Contract
from app.models.user import User
from app.permissions import BasePermissions
from app.views.contract_view import ContractView
from app.regex import is_valid_amount, is_valid_id
from sqlalchemy.orm import Session


#######################################################################################################################
#                                                    CONTRATS                                                         #
#######################################################################################################################
class ContractController(CRUDMixin):
    def __init__(self, session: Session, main_view: Any, base_view: Any) -> None:
        """
        Initialise le contrôleur de contrat avec la session SQLAlchemy, la vue principale et la vue de base.
        """
        super().__init__(session)
        self.main_view = main_view
        self.contract_view = ContractView(main_view)
        self.authenticated_user: User = main_view.authenticated_user
        self.base_view = base_view

    @Decorator.with_banner
    @BasePermissions.check_permission("is_commercial", "is_management")
    def handle_contract_menu(self) -> None:
        """
        Affiche le menu de gestion des contrats et exécute l'action sélectionnée par l'utilisateur.
        """
        while True:
            choice: str = self.contract_view.print_contract_menu()

            actions: dict[str, Optional[Any]] = {
                "1": self.list_contracts,
                "2": self.create_contract,
                "3": self.update_contract,
                "4": self.delete_contract,
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
    @BasePermissions.check_permission("is_commercial", "is_management")
    def create_contract(self) -> Optional[Contract]:
        """
        Crée un nouveau contrat pour un client donné, en s’assurant que l’utilisateur a les droits requis.
        Retourne l'objet Contract créé ou None si une erreur survient.
        """
        client_id, total_amount, commercial_id, remaining_amount, signed_input = self.contract_view.print_create_contract_view()

        if not client_id or not total_amount or not commercial_id or not remaining_amount or not signed_input:
            print("❌ Tous les champs sont obligatoires.")
            return None
        try:
            client_id = int(client_id)
            commercial_id = int(commercial_id)
            total_amount = float(total_amount)
            remaining_amount = float(remaining_amount)
        except ValueError:
            print("❌ Les montants et les IDs doivent être des nombres valides.")
            return None
        
        if signed_input.lower() not in ["oui", "non"]:
            print("❌ Valeur pour 'Signé' invalide. Utilisez 'oui' ou 'non'.")
            return None
        signed = signed_input.lower() == "oui"

        client: Optional[Client] = self.session.get(Client, client_id)
        commercial: Optional[User] = self.session.get(User, commercial_id)

        if not client:
            print("❌ Le client n'a pas été trouvé.")
            return None
        if not commercial:
            print("❌ Le commercial n'a pas été trouvé.")
            return None
        
        if self.authenticated_user.is_commercial and client.contact_commercial_id != self.authenticated_user.id:
            print("❌ Vous ne pouvez créer des contrats que pour vos clients.")
            return None

        return self.create(
            Contract,
            client=client,
            contact_commercial=commercial,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            signed=signed,
        )

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management")
    def update_contract(self) -> Optional[None]:
        """
        Met à jour un contrat existant. Seuls les utilisateurs autorisés peuvent modifier les contrats liés à leurs clients.
        """
        contracts: list[Contract] = self.list(Contract)
        contract_id: Any = self.contract_view.print_update_contract_view(contracts)

        if not is_valid_id(contract_id):
            print("❌ Invalid contract ID.")
            return None

        contract: Optional[Contract] = self.session.get(Contract, contract_id)
        if not contract:
            print("❌ Le contrat n'a pas été trouvé.")
            return None

        if self.authenticated_user.is_commercial and contract.contact_commercial_id != self.authenticated_user.id:
            print("❌ Vous ne pouvez modifier que les contrats de vos clients.")
            return None

        client_id: Any
        commercial_id: Any
        total_amount: Any
        remaining_amount: Any
        client_id, commercial_id, total_amount, remaining_amount, signed_input = self.contract_view.print_update_contract_form()

        update_data: dict[str, Any] = {}
        if is_valid_id(client_id):
            client: Optional[Client] = self.session.get(Client, client_id)
            if client:
                update_data["client"] = client
        if is_valid_id(commercial_id):
            commercial: Optional[User] = self.session.get(User, commercial_id)
            if commercial:
                update_data["contact_commercial"] = commercial
        if total_amount and is_valid_amount(total_amount):
            update_data["total_amount"] = total_amount
        if remaining_amount and is_valid_amount(remaining_amount):
            update_data["remaining_amount"] = remaining_amount

        if signed_input.lower() in ["oui", "non"]:
            update_data["signed"] = True if signed_input.lower() == "oui" else False

        if update_data:
            self.update(Contract, contract_id, **update_data)
        else:
            print("❌ Aucune modification n'a été effectuée.")
        return None

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_contract(self) -> Optional[None]:
        """
        Supprime un contrat spécifié par l'utilisateur. Seuls les utilisateurs ayant les droits de gestion peuvent supprimer.
        """
        contracts: list[Contract] = self.list(Contract)
        contract_id: Any = self.contract_view.print_delete_contract_view(contracts)

        if not is_valid_id(contract_id):
            print("❌ Invalid contract ID.")
            return None

        contract: Optional[Contract] = self.session.get(Contract, contract_id)
        if not contract:
            print("❌ Contrat introuvable.")
            return None

        return self.delete(Contract, contract_id)

    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def list_contracts(self) -> Optional[None]:
        """
        Liste tous les contrats disponibles. Accessible aux utilisateurs avec les rôles commercial, support ou management.
        """
        contracts: list[Contract] = self.list(Contract)
        if not contracts:
            print("❌ Aucun contrat n'a été trouvé.")
            return None
        return self.contract_view.print_contract_list_view(contracts)
