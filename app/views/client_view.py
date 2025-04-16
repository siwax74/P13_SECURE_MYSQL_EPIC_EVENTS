#######################################################################################################################
#                                                    CLIENTS                                                          #
#######################################################################################################################
class ClientView:
    def __init__(self, main_view):
        self.main_view = main_view

    def print_client_menu(self):
        self.main_view.print_welcome_message()
        print("\nMenu des clients :")
        print("1️⃣ - Liste des clients")
        print("2️⃣ - Ajouter un client")
        print("3️⃣ - Modifier un client")
        print("4️⃣ - Supprimer un client")
        print("-" * 50)
        print("5️⃣ - Retour au menu principal")
        choice = input("Sélectionnez une option: ")
        return choice

    def print_create_client_view(self):
        self.main_view.print_welcome_message()
        print("\n===== Création d'un nouveau client =====")
        name = input("Nom du client : ")
        email = input("Email du client : ")
        phone = input("Numéro de téléphone : ")
        company = input("Nom de l'entreprise : ")
        return name, email, phone, company

    def print_clients_list_view(self, clients):
        """Affiche la liste des clients de manière formatée."""
        self.main_view.print_welcome_message()
        print("\n📋 Liste des Clients 📋")
        for client in clients:
            print(f"🔹 ID Client            : {client.id}")
            print(f"👤 Nom                  : {client.name}")
            print(f"📧 Email                : {client.email}")
            print(f"📞 Téléphone            : {client.phone}")
            print(f"🏢 Entreprise           : {client.company}")
            print(f"📅 Créé le              : {client.created_at.strftime('%d/%m/%Y')}")
            print(f"🔄 Dernière mise à jour : {client.updated_at.strftime('%d/%m/%Y')}")
            print("-" * 50)
        print("🔙 4 - Retour au menu principal")
        choice = input("Sélectionnez une option: ")
        return choice

    def print_update_client_view(self, clients):
        self.main_view.print_welcome_message()
        print("\n📋 Liste des clients :\n")
        for client in clients:
            print(f"🔹 ID Client            : {client.id}")
            print(f"👤 Nom                  : {client.name}")
            print(f"📧 Email                : {client.email}")
            print(f"📞 Téléphone            : {client.phone}")
            print(f"🏢 Entreprise           : {client.company}")
            print(f"📅 Créé le              : {client.created_at.strftime('%d/%m/%Y')}")
            print(f"🔄 Dernière mise à jour : {client.updated_at.strftime('%d/%m/%Y')}")
            print("-" * 50)
        print("🔙 4 - Retour au menu principal")
        choice = input("✏️  Entrez l'ID du client à modifier : ")
        return choice

    def print_update_client_form(self):
        self.main_view.print_welcome_message()
        print("\n===== Modification du client =====")
        name = input("Nom : ")
        email = input("Email : ")
        phone = input("Téléphone : ")
        company = input("Entreprise : ")
        return name, email, phone, company

    def print_delete_client_view(self, clients):
        self.main_view.print_welcome_message()
        print("\n📋 Liste des clients :\n")
        for client in clients:
            print(f"🔹 ID Client            : {client.id}")
            print(f"👤 Nom                  : {client.name}")
            print(f"📧 Email                : {client.email}")
            print(f"📞 Téléphone            : {client.phone}")
            print(f"🏢 Entreprise           : {client.company}")
            print(f"📅 Créé le              : {client.created_at.strftime('%d/%m/%Y')}")
            print(f"🔄 Dernière mise à jour : {client.updated_at.strftime('%d/%m/%Y')}")
            print("-" * 50)
        print("🔙 4 - Retour au menu principal")
        choice = input("✏️  Entrez l'ID du client à supprimer : ")
        return int(choice)
