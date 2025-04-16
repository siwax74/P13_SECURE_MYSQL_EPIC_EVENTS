#######################################################################################################################
#                                                    UTILISATEURS                                                     #
#######################################################################################################################
class UserView:
    def __init__(self, main_view):
        self.main_view = main_view

    def print_user_menu(self):
        """Affiche le menu des utilisateurs."""
        self.main_view.print_welcome_message()
        print("\n👤 Menu des utilisateurs :")
        print("1️⃣ - Liste des utilisateurs")
        print("2️⃣ - Ajouter un utilisateur")
        print("3️⃣ - Modifier un utilisateur")
        print("4️⃣ - Supprimer un utilisateur")
        print("5️⃣ - Retour au menu principal")
        choice = input("Sélectionnez une option : ")
        return choice

    def print_user_list_view(self, users):
        """Affiche la liste des utilisateurs."""
        self.main_view.print_welcome_message()
        print("\n📋 Liste des utilisateurs 📋")
        for user in users:
            print(f"🆔 ID            : {user.id}")
            print(f"👤 Nom d'utilisateur : {user.username}")
            print(f"📧 Email         : {user.email}")
            print(f"🧑‍💼 Management    : {'✅' if user.is_management else '❌'}")
            print(f"💼 Commercial    : {'✅' if user.is_commercial else '❌'}")
            print(f"🎧 Support       : {'✅' if user.is_support else '❌'}")
            print("-" * 50)
        print("🔙 5 - Retour au menu principal")
        choice = input("Sélectionnez une option : ")
        return choice

    def print_create_user_view(self):
        """Affiche le formulaire pour créer un utilisateur."""
        self.print_welcome_message()
        username = input("Nom d'utilisateur : ")
        email = input("Adresse email : ")
        password = input("Mot de passe : ")

        is_management = input("Est-ce un manager ? (y/n) : ").lower() == "y"
        is_commercial = input("Est-ce un commercial ? (y/n) : ").lower() == "y"
        is_support = input("Est-ce un support ? (y/n) : ").lower() == "y"

        return username, email, password, is_management, is_commercial, is_support

    def print_update_user_view(self, users):
        """Demande quel utilisateur modifier."""
        self.print_welcome_message()
        print("\n📋 Liste des utilisateurs :")
        for user in users:
            print(f"{user.id} - {user.username} ({user.email})")
        user_id = input("Entrez l'ID de l'utilisateur à modifier : ")
        return int(user_id)

    def print_update_user_form(self):
        """Affiche le formulaire pour modifier un utilisateur."""
        self.print_welcome_message()
        username = input("Nouveau nom d'utilisateur (laisser vide pour ne pas modifier) : ")
        email = input("Nouvelle adresse email (laisser vide pour ne pas modifier) : ")
        password = input("Nouveau mot de passe (laisser vide pour ne pas modifier) : ")

        is_management_input = input("Est-ce un manager ? (y/n/ou rien pour ne pas modifier) : ").lower()
        is_management = True if is_management_input == "y" else False if is_management_input == "n" else None

        is_commercial_input = input("Est-ce un commercial ? (y/n/ou rien pour ne pas modifier) : ").lower()
        is_commercial = True if is_commercial_input == "y" else False if is_commercial_input == "n" else None

        is_support_input = input("Est-ce un support ? (y/n/ou rien pour ne pas modifier) : ").lower()
        is_support = True if is_support_input == "y" else False if is_support_input == "n" else None

        return username, email, password, is_management, is_commercial, is_support

    def print_delete_user_view(self, users):
        """Demande quel utilisateur supprimer."""
        self.print_welcome_message()
        print("\n🗑️ Liste des utilisateurs à supprimer :")
        for user in users:
            print(f"{user.id} - {user.username} ({user.email})")
        user_id = input("Entrez l'ID de l'utilisateur à supprimer : ")
        return int(user_id)
