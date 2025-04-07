from datetime import datetime
from models.client import Client
from models.contract import Contract
from models.user import User
from permissions import BasePermissions
from views.main_view import MainView


class MainController(BasePermissions):
    def __init__(self, session, authenticated_user, cli_view):
        super().__init__(authenticated_user)  # Appel au constructeur de BasePermissions
        self.session = session
        self.authenticated_user = authenticated_user
        self.cli_view = cli_view
        self.main_view = MainView(authenticated_user)

    def run(self):
        """Affiche le menu principal après connexion."""
        while True:
            user = self.authenticated_user
            self.cli_view.print_banner()
            choice = self.main_view.print_main_view()
            if choice == "1":  # Contrats
                if self.is_commercial:
                    choice = self.main_view.print_contract_menu()
                    if choice == "1":  # Liste des contrats
                        self.list_contracts()
                    elif choice == "2":  # Nouveau contrat
                        self.create_contract()
                else:
                    print("❌ Vous n'avez pas la permission d'accéder aux contrats.")

            elif choice == "2":  # Clients
                if self.authenticated_user:
                    self.cli_view.print_banner()
                    choice = self.main_view.print_client_menu()
                    if choice == "1":
                        self.cli_view.print_banner()
                        self.create_client()
                    elif choice == "2":
                        self.cli_view.print_banner()
                        self.list_clients_view()
                    elif choice == "3":
                        self.cli_view.print_banner()
                        self.update_client()

            elif choice == "3":  # Evénements
                if self.authenticated_user:
                    self.cli_view.print_banner()

    def list_contracts(self):
        """Liste les contrats"""
        self.cli_view.print_banner()
        contracts = self.session.query(Contract).all()
        self.main_view.print_contract_list(contracts)

    def create_contract(self):
        """Créer un nouveau contrat."""
        self.cli_view.print_banner()
        client_information, total_amount, commercial_id, remaining_amount = self.main_view.print_create_contract_form()

    def create_client(self):
        name, email, phone, company = self.main_view.print_create_customer_view()
        if not all([name, email, phone, company]):
            return None
        contact_commercial = (
            self.session.query(User).filter_by(is_commercial=True).first()
        )  # Récupère le premier utilisateur commercial

        if not contact_commercial:
            print("❌ Aucun contact commercial disponible.")
            return None

        try:
            client = Client(
                name=name, email=email, phone=phone, company=company, contact_commercial=contact_commercial
            )
            self.session.add(client)
            self.session.commit()
            return client.id

        except Exception as e:
            self.session.rollback()
            print(f"❌ Erreur lors de la création du client: {e}")
            return None

    def list_clients_view(self):
        """Affiche la liste des clients"""
        clients = self.session.query(Client).all()
        self.cli_view.print_banner()
        self.main_view.print_clients_list_view(clients)

    def update_client(self):
        """Met à jour un client lié à l'utilisateur connecté (contact commercial)."""

        # Récupérer les clients liés à l'utilisateur connecté
        clients = self.session.query(Client).filter(Client.contact_commercial_id == self.authenticated_user.id).all()

        if not clients:
            print("Aucun client associé à votre compte.")
            return

        # Afficher la liste et demander un choix
        self.cli_view.print_banner()
        client_id_selection = self.main_view.print_update_client_view(clients)

        if not client_id_selection:
            print("Aucune sélection effectuée.")
            return

        # Récupération du client sélectionné
        client = self.session.get(Client, client_id_selection)
        if not client:
            print("Client introuvable.")
            return
        self.cli_view.print_banner()
        # Récupérer les nouvelles infos auprès de l'utilisateur
        updated_data = self.main_view.get_client_update_data(client)

        if not updated_data:
            print("Aucune mise à jour effectuée.")
            return

        # Appliquer les mises à jour
        for field, value in updated_data.items():
            setattr(client, field, value)

        # Commit en base de données
        self.session.commit()
        print(f"Le client '{client.name}' a été mis à jour avec succès.")
