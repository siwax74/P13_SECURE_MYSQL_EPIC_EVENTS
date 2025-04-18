import re
from app.mixins import CRUDMixin
from app.decorators import Decorator
from app.models.client import Client
from app.models.contract import Contract
from app.models.user import User
from app.permissions import BasePermissions
from app.views.contract_view import ContractView


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

    ############################################### CREATE CONTRACT ###################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management")
    def create_contract(self):
        client_id, total_amount, commercial_id, remaining_amount = self.contract_view.print_create_contract_view()

        if not all([client_id, total_amount, commercial_id, remaining_amount]):
            raise ValueError("❌ Tous les champs doivent être remplis.")

        if not self.is_valid_amount(total_amount) or not self.is_valid_amount(remaining_amount):
            raise ValueError("❌ Les montants doivent être des nombres valides.")

        client = self.session.get(Client, client_id)
        commercial = self.session.get(User, commercial_id)

        if not client or not commercial:
            raise ValueError("❌ Client ou commercial introuvable.")

        self.create(
            Contract,
            client_information=client,
            contact_commercial=commercial,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            signed=False,
        )
        print(f"✅ Contrat créé avec succès pour le client {client_id}.")

    ############################################### UPDATE CONTRACT ###################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management")
    def update_contract(self):
        contracts = self.session.query(Contract).all()
        contract_id = self.contract_view.print_update_contract_view(contracts)

        contract = self.session.get(Contract, contract_id)
        if not contract:
            raise ValueError("❌ Contrat introuvable.")

        client_id, commercial_id, total_amount, remaining_amount = self.contract_view.print_update_contract_form()

        if client_id:
            client = self.session.get(Client, client_id)
            if not client:
                raise ValueError("❌ Client non trouvé.")
            self.update(Contract, contract_id, client_information=client)

        if commercial_id:
            commercial = self.session.get(User, commercial_id)
            if not commercial:
                raise ValueError("❌ Commercial non trouvé.")
            self.update(Contract, contract_id, contact_commercial=commercial)

        if total_amount and self.is_valid_amount(total_amount):
            self.update(Contract, contract_id, total_amount=total_amount)
        elif total_amount:
            raise ValueError("❌ Montant total invalide.")

        if remaining_amount and self.is_valid_amount(remaining_amount):
            self.update(Contract, contract_id, remaining_amount=remaining_amount)
        elif remaining_amount:
            raise ValueError("❌ Montant restant invalide.")

    ############################################### DELETE CONTRACT ###################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_contract(self):
        contracts = self.session.query(Contract).all()
        contract_id = self.contract_view.print_delete_contract_view(contracts)

        contract = self.session.get(Contract, contract_id)
        if not contract:
            raise ValueError("❌ Contrat introuvable.")

        self.delete(Contract, contract_id)

    ############################################### LIST CONTRACTS ####################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def list_contracts(self):
        contracts = self.session.query(Contract).all()
        self.contract_view.print_contract_list_view(contracts)

    def is_valid_amount(self, value):
        try:
            return bool(re.match(r"^\d+(\.\d{1,2})?$", str(value)))
        except ValueError:
            return False
