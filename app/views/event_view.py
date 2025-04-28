from datetime import datetime

#######################################################################################################################
#                                                    EVENEMENTS                                                       #
#######################################################################################################################


class EventView:
    def __init__(self, main_view):
        self.main_view = main_view

    def print_event_menu(self):
        """Affiche le menu des événements et affiche un message de bienvenue."""
        self.main_view.print_welcome_message()
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
        self.main_view.print_welcome_message()
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
        self.main_view.print_welcome_message()
        title = input("Titre de l'événement : ")
        client_id = input("ID du client : ")
        support_contact_id = input("ID du support contact : ")
        start_datetime = input("Date et heure de début (format: dd/mm/yyyy hh:mm) : ")
        end_datetime = input("Date et heure de fin (format: dd/mm/yyyy hh:mm) : ")
        location = input("Lieu de l'événement : ")
        attendees = input("Nombre d'invités : ")
        notes = input("Notes : ")
        start_datetime = datetime.strptime(start_datetime, "%d/%m/%Y %H:%M")
        end_datetime = datetime.strptime(end_datetime, "%d/%m/%Y %H:%M")
        return title, client_id, support_contact_id, start_datetime, end_datetime, location, attendees, notes

    def print_update_event_view(self):
        """Affiche la liste des événements et demande l'ID de l'événement à modifier."""
        self.main_view.print_welcome_message()
        print("\n📋 Liste des événements :\n")
        event_id = input("Veuillez entrer l'ID de l'événement à modifier: ")
        return int(event_id)

    def print_update_event_form(self):
        """Affiche le formulaire pour modifier un événement."""
        self.main_view.print_welcome_message()
        title = input("Nouveau titre de l'événement : ")
        client_id = input("Nouveau ID du client : ")
        support_contact_id = input("Nouveau ID du support contact : ")
        start_datetime = input("Nouvelle date et heure de début (format: dd/mm/yyyy hh:mm) : ")
        end_datetime = input("Nouvelle date et heure de fin (format: dd/mm/yyyy hh:mm) : ")
        location = input("Nouveau lieu de l'événement : ")
        attendees = input("Nouveau nombre d'invités : ")
        notes = input("Nouvelles notes : ")
        start_datetime = datetime.strptime(start_datetime, "%d/%m/%Y %H:%M")
        end_datetime = datetime.strptime(end_datetime, "%d/%m/%Y %H:%M")

        return title, client_id, support_contact_id, start_datetime, end_datetime, location, attendees, notes

    def print_delete_event_view(self):
        """Affiche la liste des événements et demande l'ID de l'événement à supprimer."""
        self.main_view.print_welcome_message()
        print("\n📋 Liste des événements :\n")
        event_id = input("Veuillez entrer l'ID de l'événement à supprimer: ")
        return int(event_id)
