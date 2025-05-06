import bcrypt
from app.decorators import Decorator
from app.mixins import CRUDMixin
from app.models.user import User
from app.permissions import BasePermissions
from app.regex import is_valid_email, is_valid_id, is_valid_password, is_valid_username
from app.views.user_view import UserView
from typing import Optional, List


#######################################################################################################################
#                                                    UTILISATEUR                                                      #
#######################################################################################################################
class UserController(CRUDMixin):
    """
    Contrôleur gérant les opérations sur les utilisateurs : création, mise à jour, suppression et liste.
    """

    def __init__(self, session, main_view, base_view) -> None:
        """
        Initialise le contrôleur des utilisateurs.

        Args:
            session (Session): Session SQLAlchemy pour les requêtes à la base de données.
            main_view (MainView): Vue principale qui affiche les menus et les informations.
            base_view (BaseView): Vue de base utilisée pour l'affichage.
        """
        super().__init__(session)
        self.base_view = base_view
        self.main_view = main_view
        self.user_view = UserView(main_view)
        self.authenticated_user = main_view.authenticated_user

    ############################################### MENU USER #########################################################
    @Decorator.with_banner
    @BasePermissions.check_permission("is_commercial", "is_management")
    def handle_user_menu(self) -> None:
        """
        Gère le menu utilisateur. Permet de choisir les actions à réaliser sur les utilisateurs.
        """
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
    def create_user(self) -> None:
        """
        Crée un nouvel utilisateur après validation des données.

        Vérifie que les données saisies sont valides et génère un mot de passe haché avant de créer l'utilisateur.
        """
        username, email, password, is_management, is_commercial, is_support = self.user_view.print_create_user_view()

        if not is_valid_username(username):
            print("❌ Veuillez renseigner un nom d'utilisateur.")
            return None
        if not is_valid_email(email):
            print("❌ Veuillez renseigner une adresse e-mail.")
            return None
        if not is_valid_password(password):
            print("❌ Veuillez renseigner un mot de passe.")
            return None

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

    def generate_hashed_password(self, plain_password: str) -> str:
        """
        Génère un mot de passe haché à partir d'un mot de passe en clair.

        Args:
            plain_password (str): Mot de passe en clair à hacher.

        Returns:
            str: Mot de passe haché.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    ############################################### UPDATE USER #######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def update_user(self) -> None:
        """
        Met à jour les informations d'un utilisateur existant.

        Vérifie les valeurs saisies avant de mettre à jour l'utilisateur.
        """
        users = self.list(User)
        user_id = self.user_view.print_update_user_view(users)
        if not is_valid_id(user_id):
            print("❌ ID utilisateur invalide.")
            return None

        user = self.session.get(User, user_id)
        if not user:
            print("❌ Utilisateur non trouvé.")
            return None

        username, email, password, is_management, is_commercial, is_support = self.user_view.print_update_user_form()

        update_data = {}
        if is_valid_username(username):
            update_data["username"] = username
        if is_valid_email(email):
            update_data["email"] = email
        if is_valid_password(password):
            update_data["password_hash"] = self.generate_hashed_password(password)
        if is_management is not None:
            update_data["is_management"] = is_management
        if is_commercial is not None:
            update_data["is_commercial"] = is_commercial
        if is_support is not None:
            update_data["is_support"] = is_support

        if update_data:
            self.update(User, user_id, **update_data)
        else:
            print("⚠️ Aucun champ à mettre à jour.")
        return None

    ############################################### DELETE USER #######################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_management")
    def delete_user(self) -> None:
        """
        Supprime un utilisateur existant après validation de son ID.
        """
        users = self.list(User)
        user_id = self.user_view.print_delete_user_view(users)
        if not is_valid_id(user_id):
            print("❌ ID utilisateur invalide.")
            return None

        user = self.session.get(User, user_id)
        if not user:
            print("❌ Utilisateur introuvable.")
            return None

        self.delete(User, user_id)

    ############################################### LIST USER #########################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    @BasePermissions.check_permission("is_commercial", "is_management")
    def list_users(self) -> Optional[List[User]]:
        """
        Liste tous les utilisateurs de la base de données et les affiche.

        Returns:
            Optional[List[User]]: Liste des utilisateurs, ou None si aucun utilisateur n'est trouvé.
        """
        users = self.list(User)
        if not users:
            print("❌ Aucun utilisateur trouvé.")
            return None
        return self.user_view.print_user_list_view(users)
