from app.decorators import Decorator
from app.mixins import CRUDMixin
from app.models.client import Client
from app.models.events import Event
from app.models.user import User
from app.models.contract import Contract
from app.permissions import BasePermissions
from app.regex import (
    is_valid_attendees,
    is_valid_datetime,
    is_valid_id,
    is_valid_location,
    is_valid_notes,
    is_valid_title,
)
from app.views.event_view import EventView

#######################################################################################################################
#                                                    EVENEMENTS                                                       #
#######################################################################################################################


class EventController(CRUDMixin):
    def __init__(self, session, main_view, base_view):
        super().__init__(session)
        self.base_view = base_view
        self.main_view = main_view
        self.event_view = EventView(main_view)
        self.authenticated_user = main_view.authenticated_user

    ############################################### MENU EVENTS #######################################################
    @Decorator.with_banner
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def handle_event_menu(self):
        while True:
            choice = self.event_view.print_event_menu()

            actions = {
                "1": self.list_events,
                "2": (self.create_event,),
                "3": (self.update_event,),
                "4": self.delete_event,
                "5": "exit",
            }

            action = actions.get(choice)
            if action == "exit":
                break
            elif action:
                action()
            else:
                print("❌ Choix invalide.")

    ############################################### CREATE EVENT ######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management")
    def create_event(self):
        title, contract_id, client_id, support_contact_id, start, end, location, attendees, notes = (
            self.event_view.print_create_event_view()
        )

        if not is_valid_title(title):
            print("❌ Titre invalide (1 à 255 caractères).")
            return None

        if not is_valid_id(contract_id):
            print("❌ ID de contrat invalide (doit être un nombre entier).")
            return None

        if not is_valid_id(client_id):
            print("❌ ID de client invalide (doit être un nombre entier).")
            return None

        if not is_valid_id(support_contact_id):
            print("❌ ID de contact support invalide (doit être un nombre entier).")
            return None

        if not is_valid_datetime(start):
            print("❌ Date de début invalide (format attendu : YYYY-MM-DD HH:MM:SS).")
            return None

        if not is_valid_datetime(end):
            print("❌ Date de fin invalide (format attendu : YYYY-MM-DD HH:MM:SS).")
            return None

        if not is_valid_location(location):
            print("❌ Lieu invalide (1 à 255 caractères).")
            return None

        if not is_valid_attendees(attendees):
            print("❌ Nombre de participants invalide (doit être un nombre entier).")
            return None

        if not is_valid_notes(notes):
            print("❌ Notes invalides (0 à 1000 caractères maximum).")
            return None

        contract = self.session.get(Contract, contract_id)
        client = self.session.get(Client, client_id)
        support_contact = self.session.get(User, support_contact_id)

        if not contract:
            print("❌ Contrat introuvable.")
            return None

        if not client:
            print("❌ Client introuvable.")
            return None

        if not support_contact:
            print("❌ Contact support introuvable.")
            return None

        if self.authenticated_user.is_commercial:
            if contract.contact_commercial_id != self.authenticated_user.id:
                print("❌ Vous ne pouvez créer un événement que pour vos propres contrats.")
                return None
            if not contract.signed:
                print("❌ Impossible de créer un événement pour un contrat non signé.")
                return None

        self.create(
            Event,
            title=title,
            contract_id=contract_id,
            client=client,
            support_contact=support_contact,
            start_datetime=start,
            end_datetime=end,
            location=location,
            attendees=attendees,
            notes=notes,
        )

    ############################################### UPDATE EVENT ######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_support", "is_management")
    def update_event(self):
        events = self.list(Event)
        event_id = self.event_view.print_update_event_view(events)

        if not is_valid_id(event_id):
            print("❌ ID d'événement invalide.")
            return None

        event = self.session.get(Event, event_id)
        if not event:
            print("❌ Événement introuvable.")
            return None

        if self.authenticated_user.is_support and event.support_contact_id != self.authenticated_user.id:
            print("❌ Vous n'êtes pas autorisé à modifier cet événement.")
            return None

        (title, contract_id, client_id, support_contact_id, start, end, location, attendees, notes) = (
            self.event_view.print_update_event_form()
        )

        update_data = {}
        if title and is_valid_title(title):
            update_data["title"] = title
        if contract_id and is_valid_id(contract_id):
            update_data["contract_id"] = contract_id
        if client_id and is_valid_id(client_id):
            update_data["client_id"] = client_id
        if support_contact_id and is_valid_id(support_contact_id):
            update_data["support_contact_id"] = support_contact_id
        if start and is_valid_datetime(start):
            update_data["start_datetime"] = start
        if end and is_valid_datetime(end):
            update_data["end_datetime"] = end
        if location and is_valid_location(location):
            update_data["location"] = location
        if attendees and is_valid_attendees(attendees):
            update_data["attendees"] = attendees
        if notes and is_valid_notes(notes):
            update_data["notes"] = notes

        if update_data:
            self.update(Event, event_id, **update_data)
        else:
            print("⚠️ Aucun champ valide à mettre à jour.")
        return None

    ############################################### DELETE EVENT ######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_event(self):
        events = self.list(Event)
        event_id = self.event_view.print_delete_event_view(events)

        if not is_valid_id(event_id):
            print("❌ ID d'événement invalide.")
            return None

        event = self.session.get(Event, event_id)
        if not event:
            print("❌ Événement introuvable.")
            return None

        self.delete(Event, event_id)

    ############################################### LIST EVENTS #######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def list_events(self):
        events = self.list(Event)

        if self.authenticated_user.is_commercial:
            events = [e for e in events if e.contract.contact_commercial_id == self.authenticated_user.id]
        elif self.authenticated_user.is_support:
            events = [e for e in events if e.support_contact_id == self.authenticated_user.id]

        if not events:
            print("❌ Aucun événement trouvé.")
            return None

        return self.event_view.print_events_list_view(events)
