from app.decorators import Decorator
from app.mixins import CRUDMixin
from app.models.client import Client
from app.models.events import Event
from app.models.user import User
from app.permissions import BasePermissions
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
    @BasePermissions.check_permission("is_commercial", "is_management")
    def handle_event_menu(self):
        while True:
            choice = self.event_view.print_event_menu()

            actions = {
                "1": self.list_events,
                "2": self.create_event,
                "3": self.update_event,
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
    @BasePermissions.check_permission("is_commercial")
    def create_event(self):
        self.base_view.print_banner()
        data = self.event_view.print_create_event_view()
        if not all(data):
            raise ValueError("❌ Tous les champs sont obligatoires.")

        title, contract_id, client_id, support_contact_id, start, end, location, attendees, notes = data

        client = self.session.get(Client, client_id)
        support_contact = self.session.get(User, support_contact_id)

        if not client or not support_contact:
            raise ValueError("❌ Client ou contact de support introuvable.")

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

    ############################################### UPDATE EVENT #####################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management", "is_support")
    def update_event(self):
        events = self.list(Event)
        event_id = self.event_view.print_update_event_view(events)
        event = self.session.get(Event, event_id)

        if not event:
            raise ValueError("❌ Événement introuvable.")

        updated_data = self.event_view.print_update_event_form(event)
        if not updated_data:
            raise ValueError("❌ Aucune donnée à mettre à jour.")

        self.update(Event, event_id, updated_data)

    ############################################### DELETE EVENT ######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_event(self):
        events = self.list(Event)
        event_id = self.event_view.print_delete_event_view(events)

        event = self.session.get(Event, event_id)
        if not event:
            raise ValueError("❌ Événement introuvable.")

        self.delete(Event, event_id)

    ############################################### LIST EVENTS #######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management", "is_support")
    def list_events(self):
        events = self.list(Client)
        self.base_view.print_banner()
        self.event_view.print_events_list_view(events)
