import bcrypt
from app.decorators import Decorator
from app.mixins import CRUDMixin
from app.models.user import User
from app.permissions import BasePermissions
from app.views.user_view import UserView


#######################################################################################################################
#                                                    UTILISATEUR                                                      #
#######################################################################################################################
class UserController(CRUDMixin):
    def __init__(self, session, main_view, base_view):
        super().__init__(session)
        self.base_view = base_view
        self.main_view = main_view
        self.user_view = UserView(main_view)
        self.authenticated_user = main_view.authenticated_user

    ############################################### MENU USER #########################################################
    @Decorator.with_banner
    @BasePermissions.check_permission("is_commercial", "is_management")
    def handle_user_menu(self):
        while True:
            choice = self.user_view.print_user_menu()

            actions = {
                "1": self.list_users,
                "2": self.create_user,
                "3": self.update_user,
                "4": self.delete_user,
                "5": "exit",
            }

            action = actions.get(choice)
            if action == "exit":
                break
            elif action:
                action()
            else:
                print("❌ Choix invalide.")

    ############################################### CREATE USER #######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def create_user(self):
        username, email, password, is_management, is_commercial, is_support = self.user_view.print_create_user_view()

        if not all([username, email, password]):
            raise ValueError("❌ Les champs 'username', 'email' et 'mot de passe' sont obligatoires.")

        password_hash = self.generate_hashed_password(password)

        self.create(
            User,
            username=username,
            email=email,
            password_hash=password_hash,
            is_management=is_management,
            is_commercial=is_commercial,
            is_support=is_support,
        )
        print(f"✅ Utilisateur '{username}' créé avec succès.")

    def generate_hashed_password(plain_password: str):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), salt)

        return hashed_password.decode("utf-8")

    ############################################### UPDATE USER #######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def update_user(self):
        users = self.list(User)
        user_id = self.user_view.print_update_user_view(users)

        user = self.session.get(User, user_id)
        if not user:
            raise ValueError("❌ Utilisateur introuvable.")

        username, email, password, is_management, is_commercial, is_support = self.main_view.print_update_user_form()

        if username:
            self.update(User, user_id, username=username)
        if email:
            self.update(User, user_id, email=email)
        if password:
            password_hash = self.generate_hashed_password(password)
            self.update(User, user_id, password_hash=password_hash)
        if is_management is not None:
            self.update(User, user_id, is_management=is_management)
        if is_commercial is not None:
            self.update(User, user_id, is_commercial=is_commercial)
        if is_support is not None:
            self.update(User, user_id, is_support=is_support)

        print(f"✅ Utilisateur '{user.username}' mis à jour.")

    ############################################### DELETE USER #######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_user(self):
        users = self.list(User)
        user_id = self.user_view.print_delete_user_view(users)

        user = self.session.get(User, user_id)
        if not user:
            raise ValueError("❌ Utilisateur introuvable.")

        self.delete(User, user_id)
        print(f"✅ Utilisateur '{user.username}' supprimé.")

    ############################################### LIST USER #########################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def list_users(self):
        users = self.list(User)
        self.user_view.print_user_list_view(users)
