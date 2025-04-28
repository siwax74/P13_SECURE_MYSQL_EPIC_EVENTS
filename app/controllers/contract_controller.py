import re
from app.mixins import CRUDMixin
from app.decorators import Decorator
from app.models.client import Client
from app.models.contract import Contract
from app.models.user import User
from app.permissions import BasePermissions
from app.views.contract_view import ContractView
from app.regex import is_valid_amount, is_valid_id


#######################################################################################################################
#                                                    CONTRATS                                                         #
#######################################################################################################################
class ContractController(CRUDMixin):
    def __init__(self, session, main_view, base_view):
        super().__init__(session)
        self.main_view = main_view
        self.contract_view = ContractView(main_view)
        self.authenticated_user = main_view.authenticated_user
        self.base_view = base_view

    ############################################### MENU CONTRACTS ####################################################
    @Decorator.with_banner
    @BasePermissions.check_permission("is_commercial", "is_management")
    def handle_contract_menu(self):
        while True:
            choice = self.contract_view.print_contract_menu()

            actions = {
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

    ############################################### CREATE CONTRACT ###################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management")
    def create_contract(self):
        client_id, total_amount, commercial_id, remaining_amount = self.contract_view.print_create_contract_view()

        if not client_id or not total_amount or not commercial_id or not remaining_amount:
            print("❌ Tous les champs sont obligatoires.")
            return None

        client = self.session.get(Client, client_id)
        commercial = self.session.get(User, commercial_id)

        if not client:
            print("❌ Le client n'a pas été trouvé.")
            return None
        if not commercial:
            print("❌ Le commercial n'a pas été trouvé.")
            return None

        # Vérifie que le commercial connecté crée un contrat pour son propre client
        if self.authenticated_user.is_commercial and client.contact_commercial_id != self.authenticated_user.id:
            print("❌ Vous ne pouvez créer des contrats que pour vos clients.")
            return None

        return self.create(
            Contract,
            client_information=client,
            contact_commercial=commercial,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            signed=False,
        )

    ############################################### UPDATE CONTRACT ###################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management")
    def update_contract(self):
        contracts = self.list(Contract)
        contract_id = self.contract_view.print_update_contract_view(contracts)
        if not is_valid_id(contract_id):
            print("❌ Invalid contract ID.")
            return None
        contract = self.session.get(Contract, contract_id)
        if not contract:
            print("❌ Le contrat n'a pas été trouvé.")
            return None

        if self.authenticated_user.is_commercial and contract.contact_commercial_id != self.authenticated_user.id:
            print("❌ Vous ne pouvez modifier que les contrats de vos clients.")
            return None

        client_id, commercial_id, total_amount, remaining_amount = self.contract_view.print_update_contract_form()

        update_data = {}
        if is_valid_id(client_id):
            client = self.session.get(Client, client_id)
            if client:
                update_data["client_information"] = client
        if is_valid_id(commercial_id):
            commercial = self.session.get(User, commercial_id)
            if commercial:
                update_data["contact_commercial"] = commercial
        if total_amount and is_valid_amount(total_amount):
            update_data["total_amount"] = total_amount
        if remaining_amount and is_valid_amount(remaining_amount):
            update_data["remaining_amount"] = remaining_amount

        if update_data:
            self.update(Contract, contract_id, **update_data)
        else:
            print("❌ Aucune modification n'a été effectuée.")
        return None

    ############################################### DELETE CONTRACT ###################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_contract(self):
        contracts = self.list(Contract)
        contract_id = self.contract_view.print_delete_contract_view(contracts)
        if not is_valid_id(contract_id):
            print("❌ Invalid contract ID.")
            return None

        contract = self.session.get(Contract, contract_id)
        if not contract:
            print("❌ Contrat introuvable.")
            return None

        return self.delete(Contract, contract_id)

    ############################################### LIST CONTRACTS ####################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def list_contracts(self):
        contracts = self.list(Contract)
        if not contracts:
            print("❌ Aucun contrat n'a été trouvé.")
            return None
        return self.contract_view.print_contract_list_view(contracts)
