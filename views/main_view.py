from datetime import datetime


class MainView:
    def __init__(self, authenticated_user):
        self.authenticated_user = authenticated_user

    def print_welcome_message(self):
        """Affiche un message de bienvenue général."""
        if self.authenticated_user:
            print(f"\n👋 Bienvenue, {self.authenticated_user.email} !")
        else:
            print("\n👋 Bienvenue !")

    def print_main_view(self):
        """Affiche le menu principal après connexion et gère les choix de l'utilisateur."""
        self.print_welcome_message()
        print("\n===== MENU PRINCIPAL =====")
        print("1️⃣ - Contrats")
        print("2️⃣ - Clients")
        print("3️⃣ - Evénements")
        print("4️⃣ - Déconnexion")
        choice = input("\nSélectionnez une option: ")
        return choice

    #######################################################################################################################
    #                                                    CONTRATS                                                         #
    #######################################################################################################################
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

    def print_contract_list_view(self, contracts):
        print("\n📄 Liste des contrats :\n")
        for contract in contracts:
            print(f"🔹 Contrat ID : {contract.id}")
            print(
                f"    🧾 Client        : {contract.client_information.name if contract.client_information else 'Inconnu'}"
            )
            print(f"    💰 Montant total : {contract.total_amount} €")
            print(
                f"    💼 Commercial     : {contract.contact_commercial.email if contract.contact_commercial else 'N/A'}"
            )
            print(f"    🧾 Restant dû    : {contract.remaining_amount} €")
            print(f"    📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
            print(f"    🔐 Signé         : {'Oui' if contract.signed else 'Non'}")
            print("-" * 50)
            print(f"4️⃣ - Retour au menu principal")
            choice = input("Sélectionnez une option: ")
            return choice

    def print_create_contract_view(self):
        print("\n===== Création d'un nouveau contrat =====")
        client_information = input("Id du client : ")
        total_amount = input("Coût total : ")
        commercial_id = input("Id du commercial : ")
        remaining_amount = input("Remise total : ")
        return client_information, total_amount, commercial_id, remaining_amount

    def print_update_contract_view(self, contracts):
        print("\n📄 Liste des contrats :\n")
        for contract in contracts:
            print(f"🔹 Contrat ID : {contract.id}")
            print(
                f"    🧾 Client        : {contract.client_information if contract.client_information else 'Inconnu'}"
            )
            print(f"    💰 Montant total : {contract.total_amount} €")
            print(f"    💼 Commercial     : {contract.contact_commercial if contract.contact_commercial else 'N/A'}")
            print(f"    🧾 Restant dû    : {contract.remaining_amount} €")
            print(f"    📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
            print(f"    🔐 Signé         : {'Oui' if contract.signed else 'Non'}")
            print("-" * 50)
            print(f"4️⃣ - Retour au menu principal")
        choice = input("Veuillez entrez l'id du contrat a modifier: ")
        return int(choice)

    def print_update_contract_form(self):
        print("\n===== Modification du contrat =====")
        client_information = input("Id du client : ")
        total_amount = input("Coût total : ")
        contact_commercial = input("Id du commercial : ")
        remaining_amount = input("Remise total : ")
        return client_information, total_amount, contact_commercial, remaining_amount

    def print_delete_contract_view(self, contracts):
        print("\n📄 Liste des contrats :\n")
        for contract in contracts:
            print(f"🔹 Contrat ID : {contract.id}")
            print(
                f"    🧾 Client        : {contract.client_information if contract.client_information else 'Inconnu'}"
            )
            print(f"    💰 Montant total : {contract.total_amount} €")
            print(f"    💼 Commercial     : {contract.contact_commercial if contract.contact_commercial else 'N/A'}")
            print(f"    🧾 Restant dû    : {contract.remaining_amount} €")
            print(f"    📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
            print(f"    🔐 Signé         : {'Oui' if contract.signed else 'Non'}")
            print("-" * 50)
            print("🔙 4 - Retour au menu principal")
        choice = input("Veuillez entrez l'id du contrat a supprimer: ")
        return int(choice)

    #######################################################################################################################
    #                                                    CLIENTS                                                          #
    #######################################################################################################################

    def print_client_menu(self):
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
        print("\n===== Création d'un nouveau client =====")
        name = input("Nom du client : ")
        email = input("Email du client : ")
        phone = input("Numéro de téléphone : ")
        company = input("Nom de l'entreprise : ")
        return name, email, phone, company

    def print_clients_list_view(self, clients):
        """Affiche la liste des clients de manière formatée."""
        print("\n📋 Liste des Clients 📋")
        for client in clients:
            print(f"🔹 ID Client       : {client.id}")
            print(f"👤 Nom             : {client.name}")
            print(f"📧 Email           : {client.email}")
            print(f"📞 Téléphone       : {client.phone}")
            print(f"🏢 Entreprise      : {client.company}")
            print(f"📅 Créé le         : {client.created_at.strftime('%d/%m/%Y')}")
            print(f"🔄 Dernière mise à jour : {client.updated_at.strftime('%d/%m/%Y')}")
            print("-" * 50)
        print("🔙 4 - Retour au menu principal")
        choice = input("Sélectionnez une option: ")
        return choice

    def print_update_client_view(self, clients):
        print("\n📋 Liste des clients :\n")
        for client in clients:
            print(f"🔹 ID Client       : {client.id}")
            print(f"👤 Nom             : {client.name}")
            print(f"📧 Email           : {client.email}")
            print(f"📞 Téléphone       : {client.phone}")
            print(f"🏢 Entreprise      : {client.company}")
            print(f"📅 Créé le         : {client.created_at.strftime('%d/%m/%Y')}")
            print(f"🔄 Dernière mise à jour : {client.updated_at.strftime('%d/%m/%Y')}")
            print("-" * 50)
        print("🔙 4 - Retour au menu principal")
        choice = input("✏️  Entrez l'ID du client à modifier : ")
        return choice

    def print_update_client_form(self):
        print("\n===== Modification du client =====")
        name = input("Nom : ")
        email = input("Email : ")
        phone = input("Téléphone : ")
        company = input("Entreprise : ")
        return name, email, phone, company

    def print_delete_client_view(self, clients):
        print("\n📋 Liste des clients :\n")
        for client in clients:
            print(f"🔹 ID Client       : {client.id}")
            print(f"👤 Nom             : {client.name}")
            print(f"📧 Email           : {client.email}")
            print(f"📞 Téléphone       : {client.phone}")
            print(f"🏢 Entreprise      : {client.company}")
            print(f"📅 Créé le         : {client.created_at.strftime('%d/%m/%Y')}")
            print(f"🔄 Dernière mise à jour : {client.updated_at.strftime('%d/%m/%Y')}")
            print("-" * 50)
        print("🔙 4 - Retour au menu principal")
        choice = input("✏️  Entrez l'ID du client à supprimer : ")
        return int(choice)

    #######################################################################################################################
    #                                                    EVENEMENTS                                                         #
    #######################################################################################################################
    def print_event_menu(self):
        """Affiche le menu des événements et affiche un message de bienvenue."""
        self.print_welcome_message()  # Message de bienvenue
        print("\nMenu des événements :")
        print("1️⃣ - Liste des événements")
        print("2️⃣ - Ajouter un événement")
        print("3️⃣ - Modifier un événement")
        print("4️⃣ - Supprimer un événement")
        print("5️⃣ - Retour au menu principal")
        choice = input("Sélectionnez une option: ")
        return choice

    def print_events_list_view(self, events):
        """Affiche la liste des événements."""
        self.print_welcome_message()  # Message de bienvenue
        print("\n📋 Liste des événements 📋")
        for event in events:
            print(f"🔹 ID Événement       : {event.event_id}")
            print(f"📅 Titre              : {event.title}")
            print(f"📍 Lieu               : {event.location}")
            print(f"⏰ Début              : {event.start_datetime.strftime('%d/%m/%Y %H:%M')}")
            print(f"⏰ Fin                : {event.end_datetime.strftime('%d/%m/%Y %H:%M')}")
            print(f"👤 Support            : {event.support_contact.email if event.support_contact else 'N/A'}")
            print(f"🧑‍🤝‍🧑 Nombre d'invités : {event.attendees}")
            print("-" * 50)
        print("🔙 4 - Retour au menu principal")
        choice = input("Sélectionnez une option: ")
        return choice

    def print_create_event_view(self):
        """Affiche le formulaire pour créer un nouvel événement."""
        self.print_welcome_message()  # Message de bienvenue
        title = input("Titre de l'événement : ")
        event_id = input("ID de l'événement : ")
        client_id = input("ID du client : ")
        support_contact_id = input("ID du support contact : ")
        start_datetime = input("Date et heure de début (format: dd/mm/yyyy hh:mm) : ")
        end_datetime = input("Date et heure de fin (format: dd/mm/yyyy hh:mm) : ")
        location = input("Lieu de l'événement : ")
        attendees = input("Nombre d'invités : ")
        notes = input("Notes : ")

        # Convertir les dates et heures en objet datetime
        start_datetime = datetime.strptime(start_datetime, "%d/%m/%Y %H:%M")
        end_datetime = datetime.strptime(end_datetime, "%d/%m/%Y %H:%M")

        return title, event_id, client_id, support_contact_id, start_datetime, end_datetime, location, attendees, notes

    def print_update_event_view(self):
        """Affiche la liste des événements et demande l'ID de l'événement à modifier."""
        self.print_welcome_message()  # Message de bienvenue
        print("\n📋 Liste des événements :\n")
        # Afficher les événements comme dans `print_event_list_view`
        event_id = input("Veuillez entrer l'ID de l'événement à modifier: ")
        return int(event_id)

    def print_update_event_form(self):
        """Affiche le formulaire pour modifier un événement."""
        self.print_welcome_message()  # Message de bienvenue
        title = input("Nouveau titre de l'événement : ")
        client_id = input("Nouveau ID du client : ")
        support_contact_id = input("Nouveau ID du support contact : ")
        start_datetime = input("Nouvelle date et heure de début (format: dd/mm/yyyy hh:mm) : ")
        end_datetime = input("Nouvelle date et heure de fin (format: dd/mm/yyyy hh:mm) : ")
        location = input("Nouveau lieu de l'événement : ")
        attendees = input("Nouveau nombre d'invités : ")
        notes = input("Nouvelles notes : ")

        # Convertir les dates et heures en objet datetime
        start_datetime = datetime.strptime(start_datetime, "%d/%m/%Y %H:%M")
        end_datetime = datetime.strptime(end_datetime, "%d/%m/%Y %H:%M")

        return title, client_id, support_contact_id, start_datetime, end_datetime, location, attendees, notes

    def print_delete_event_view(self):
        """Affiche la liste des événements et demande l'ID de l'événement à supprimer."""
        self.print_welcome_message()  # Message de bienvenue
        print("\n📋 Liste des événements :\n")
        # Afficher les événements comme dans `print_event_list_view`
        event_id = input("Veuillez entrer l'ID de l'événement à supprimer: ")
        return int(event_id)
