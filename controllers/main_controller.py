from datetime import datetime
from mixins import CRUDMixin
from models.client import Client
from models.contract import Contract
from models.events import Event
from models.user import User
from permissions import BasePermissions
from views.main_view import MainView


class MainController(BasePermissions, CRUDMixin):
    def __init__(self, session, authenticated_user, cli_view):
        super().__init__(authenticated_user)
        self.session = session
        self.authenticated_user = authenticated_user
        self.cli_view = cli_view
        self.main_view = MainView(authenticated_user)

    def run(self):
        while True:
            user = self.authenticated_user
            self.cli_view.print_banner()
            choice = self.main_view.print_main_view()
            if choice == "1":  # Contrats
                self.cli_view.print_banner()
                choice = self.main_view.print_contract_menu()
                if choice == "1":
                    self.cli_view.print_banner()
                    self.list_contracts()
                elif choice == "2":
                    self.cli_view.print_banner()
                    self.create_contract()
                elif choice == "3":
                    self.cli_view.print_banner()
                    self.update_contract()
                elif choice == "4":
                    self.cli_view.print_banner()
                    self.delete_contract()
                else:
                    print("❌ Vous n'avez pas la permission d'accéder aux contrats.")

            elif choice == "2":  # Clients
                if self.authenticated_user:
                    self.cli_view.print_banner()
                    choice = self.main_view.print_client_menu()
                    if choice == "1":
                        self.cli_view.print_banner()
                        self.list_clients()
                    elif choice == "2":
                        self.cli_view.print_banner()
                        self.create_client()
                    elif choice == "3":
                        self.cli_view.print_banner()
                        self.update_client()
                    elif choice == "4":
                        self.cli_view.print_banner()
                        self.delete_client()

            elif choice == "3":  # Événements
                if self.authenticated_user:
                    self.cli_view.print_banner()
                    choice = self.main_view.print_event_menu()
                    if choice == "1":
                        self.cli_view.print_banner()
                        self.list_events()
                    elif choice == "2":
                        self.cli_view.print_banner()
                        self.create_event()
                    elif choice == "3":
                        self.cli_view.print_banner()
                        self.update_event()
                    elif choice == "4":
                        self.cli_view.print_banner()
                        self.delete_event()

    # CONTRATS
    @BasePermissions.check_permission("is_commercial", "is_management")
    def create_contract(self):
        client_id, total_amount, commercial_id, remaining_amount = self.main_view.print_create_contract_view()
        if not all([client_id, total_amount, commercial_id, remaining_amount]):
            return None
        contract_data = {
            "client_information": self.session.get(Client, client_id),
            "contact_commercial": self.session.get(User, commercial_id),
            "total_amount": total_amount,
            "remaining_amount": remaining_amount,
            "signed": False,
        }
        self.create(Contract, contract_data)

    def update_contract(self):
        contracts = self.list(Contract)
        contract_id = self.main_view.print_update_contract_view(contracts)
        client_id, commercial_id, total_amount, remaining_amount = self.main_view.print_update_contract_form()
        updated_data = {
            "client_information": self.session.get(Client, client_id),
            "contact_commercial": self.session.get(User, commercial_id),
            "total_amount": total_amount,
            "remaining_amount": remaining_amount,
        }
        self.update(Contract, contract_id, updated_data)

    def delete_contract(self):
        contracts = self.list(Contract)
        contract_id = self.main_view.print_delete_contract_view(contracts)
        self.delete(Contract, contract_id)

    @BasePermissions.check_permission("is_commercial", "is_management")
    def list_contracts(self):
        contracts = self.list(Contract)
        self.main_view.print_contract_list_view(contracts)

    # CLIENTS
    def create_client(self):
        name, email, phone, company = self.main_view.print_create_client_view()
        if not all([name, email, phone, company]):
            return None
        client_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            "contact_commercial": self.session.query(User).filter_by(is_commercial=True).first(),
        }
        self.create(Client, client_data)

    def update_client(self):
        clients = self.list(Client)
        client_id = self.main_view.print_update_client_view(clients)
        name, email, phone, company = self.main_view.print_update_client_form()
        updated_data = {"name": name, "email": email, "phone": phone, "company": company}
        self.update(Client, client_id, updated_data)

    def delete_client(self):
        clients = self.list(Client)
        client_id = self.main_view.print_delete_client_view(clients)
        self.delete(Client, client_id)

    def list_clients(self):
        clients = self.list(Client)
        self.cli_view.print_banner()
        self.main_view.print_clients_list_view(clients)

    # EVENTS
    def create_event(self):
        self.cli_view.print_banner()
        event_data = self.main_view.print_create_event_view()
        if not all(event_data.values()):
            return None
        self.create(Event, event_data)

    def update_event(self):
        events = self.list(Event)
        event_id = self.main_view.print_update_event_view(events)
        updated_data = self.main_view.print_update_event_form(self.session.get(Event, event_id))
        self.update(Event, event_id, updated_data)

    def delete_event(self):
        events = self.list(Event)
        event_id = self.main_view.print_delete_event_view(events)
        self.delete(Event, event_id)

    def list_events(self):
        events = self.list(Event)
        self.cli_view.print_banner()
        self.main_view.print_events_list_view(events)
