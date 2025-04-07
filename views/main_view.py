class MainView:
    def __init__(self, authenticated_user):
        self.authenticated_user = authenticated_user

    def print_main_view(self):
        """Affiche le menu principal après connexion et gère les choix de l'utilisateur."""
        print(f"\n👋 Bienvenue, {self.authenticated_user.email} !")
        print("\n===== MENU PRINCIPAL =====")

        print("1️⃣ - Contrats")
        print("2️⃣ - Clients")
        print("3️⃣ - Evénements")
        print("4️⃣ - Déconnexion")

        choice = input("\nSélectionnez une option: ")
        return choice

    def print_client_menu(self):
        """Affiche le menu des clients"""
        print("\n===== MENU CLIENTS =====")
        print("1️⃣ - Ajouter un client")
        print("2️⃣ - Afficher les clients")
        print("3️⃣ - Modifier un client")
        print("4️⃣ - Retour au menu principal")

        choice = input("\nSélectionnez une option: ")
        return choice

    def print_create_client_view(self):
        print("\n===== Création d'un nouveau client =====")
        name = input("Nom du client : ")
        email = input("Email du client : ")
        phone = input("Numéro de téléphone : ")
        company = input("Nom de l'entreprise : ")
        return name, email, phone, company

    def print_clients_list_view(self, clients):
        """Affiche la liste des clients de manière formatée."""
        if not clients:
            print("❌ Aucun client trouvé.")
            return

        print("\n📋 Liste des Clients 📋")
        print("=" * 50)
        for client in clients:
            print(f"🆔 ID: {client.id}")
            print(f"🏢 Société: {client.company}")
            print(f"👤 Nom: {client.name}")
            print(f"📧 Email: {client.email}")
            print(f"📞 Téléphone: {client.phone}")
            if client.contact_commercial:
                print(f"🤝 Commercial: {client.contact_commercial.username} ({client.contact_commercial.email})")
            else:
                print("🤝 Commercial: Non assigné")
            print("-" * 50)
            print(f"4️⃣ - Retour au menu principal")
            choice = input("Sélectionnez une option: ")
            return choice

    def print_update_client_view(self, clients):
        print("\nListe des clients :")
        for idx, client in enumerate(clients, start=1):
            print(f"{idx}. {client.name} ({client.email})")

        try:
            selection = int(input("\nEntrez le numéro du client à modifier : ")) - 1
            if 0 <= selection < len(clients):
                return clients[selection].id
        except ValueError:
            pass
        return None

    def get_client_update_data(self, client):
        print(f"\n--- Mise à jour du client : {client.name} ---")
        fields = {}

        new_name = input(f"Nom [{client.name}] : ").strip()
        if new_name:
            fields["name"] = new_name

        new_email = input(f"Email [{client.email}] : ").strip()
        if new_email:
            fields["email"] = new_email

        new_phone = input(f"Téléphone [{client.phone}] : ").strip()
        if new_phone:
            fields["phone"] = new_phone

        new_company = input(f"Société [{client.company}] : ").strip()
        if new_company:
            fields["company"] = new_company

        return fields

    def print_contract_menu(self):
        print("\nMenu des contrats :")
        print("1️⃣ - Liste des contrats")
        print("2️⃣ - Ajouter un contrat")
        print("3️⃣ - Modifier un contrat")
        print("4️⃣ - Supprimer un contrat")
        print("-" * 50)
        print("5️⃣ - Retour au menu principal")
        choice = input("Sélectionnez une option: ")
        return choice

def print_contract_list(self, contracts):
    if not contracts:
        print("📭 Aucun contrat trouvé.")
        return

    print("\n📄 Liste des contrats :\n")
    for contract in contracts:
        print(f"🔹 Contrat ID : {contract.id}")
        print(f"    🧾 Client        : {contract.client.name if contract.client else 'Inconnu'}")
        print(f"    💰 Montant total : {contract.total_amount} €")
        print(f"    💼 Commercial     : {contract.commercial.username if contract.commercial else 'N/A'}")
        print(f"    🧾 Restant dû    : {contract.remaining_amount} €")
        print(f"    📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
        print(f"    🔐 Signé         : {'Oui' if contract.is_signed else 'Non'}")
        print("-" * 50)
