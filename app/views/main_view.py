class MainView:
    def __init__(self, authenticated_user):
        self.authenticated_user = authenticated_user

    def print_welcome_message(self):
        """Affiche un message de bienvenue général."""
        if self.authenticated_user:
            if self.authenticated_user.is_commercial:
                print(f"\n👋 Bienvenue, {self.authenticated_user.email} - Permissions: Is_Commercial")
            elif self.authenticated_user.is_support:
                print(f"\n👋 Bienvenue, {self.authenticated_user.email} - Permissions: Is_Support")
            elif self.authenticated_user.is_management:
                print(f"\n👋 Bienvenue, {self.authenticated_user.email} - Permissions: Is_Management")
        else:
            print("\n👋 Bienvenue !")

    def print_main_view(self):
        """Affiche le menu principal après connexion et gère les choix de l'utilisateur."""
        self.print_welcome_message()
        print("\n===== MENU PRINCIPAL =====")
        print("1️⃣ - Contrats")
        print("2️⃣ - Clients")
        print("3️⃣ - Evénements")
        print("4️⃣ - Utilisateurs")
        print("5️⃣ - Déconnexion")
        choice = input("\nSélectionnez une option: ")
        return choice
