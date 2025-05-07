from datetime import datetime

#######################################################################################################################
#                                                    CONTRATS                                                         #
#######################################################################################################################


class ContractView:
    def __init__(self, main_view):
        self.main_view = main_view

    def print_contract_menu(self):
        """Affiche le menu des contrats et affiche un message de bienvenue."""
        self.main_view.print_welcome_message()
        print("\n📑 Menu des contrats 📑 :")
        print("1️⃣ - Liste des contrats")
        print("2️⃣ - Ajouter un contrat")
        print("3️⃣ - Modifier un contrat")
        print("4️⃣ - Supprimer un contrat")
        print("🔙 5️⃣ - Retour au menu principal")
        choice = input("Sélectionnez une option : ")
        return choice

    def print_contract_list_view(self, contracts):
        """Affiche la liste des contrats."""
        self.main_view.print_welcome_message()
        print("\n📋 Liste des contrats 📋 :")
        for contract in contracts:
            print(f"🔹 Contrat ID       : {contract.id}")
            print(f"🧾 Client           : {contract.client.name if contract.client else 'Inconnu'}")
            print(f"💰 Montant total    : {contract.total_amount} €")
            print(
                f"💼 Commercial       : {contract.contact_commercial.email if contract.contact_commercial else 'N/A'}"
            )
            print(f"🧾 Restant dû       : {contract.remaining_amount} €")
            print(f"📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
            print(f"🔐 Signé            : {'Oui' if contract.signed else 'Non'}")
            print("-" * 50)
        print("🔙 4 - Retour au menu principal")
        choice = input("Sélectionnez une option : ")
        return choice

    def print_create_contract_view(self):
        """Affiche le formulaire pour créer un nouveau contrat."""
        self.main_view.print_welcome_message()
        print("\n📝 Création d'un nouveau contrat 📝")
        client = input("👥 ID du client : ")
        total_amount = input(f"💰 Montant total    :")
        commercial_id = input("💼 ID du commercial : ")
        remaining_amount = input(f"🧾 Restant dû   : ")
        signed = input("🔐 Signé ? (oui/non) : ")
        return client, total_amount, commercial_id, remaining_amount, signed

    def print_update_contract_view(self, contracts):
        """Affiche la liste des contrats et demande l'ID du contrat à modifier."""
        self.main_view.print_welcome_message()
        print("\n📋 Liste des contrats 📋 :")
        for contract in contracts:
            print(f"🔹 Contrat ID       : {contract.id}")
            print(f"🧾 Client           : {contract.client.name if contract.client else 'Inconnu'}")
            print(f"💰 Montant total    : {contract.total_amount} €")
            print(
                f"💼 Commercial       : {contract.contact_commercial.email if contract.contact_commercial else 'N/A'}"
            )
            print(f"🧾 Restant dû       : {contract.remaining_amount} €")
            print(f"📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
            print(f"🔐 Signé            : {'Oui' if contract.signed else 'Non'}")
            print("-" * 50)
        choice = input("⚙️ Veuillez entrer l'ID du contrat à modifier : ")
        return int(choice)

    def print_update_contract_form(self):
        """Formulaire pour mettre à jour un contrat."""
        client = input("👥 Nouveau ID du client (laisser vide pour ne pas changer) : ")
        commercial_id = input("💼 Nouveau ID du commercial (laisser vide pour ne pas changer) : ")
        total_amount = input("💰 Nouveau montant total (laisser vide pour ne pas changer) : ")
        remaining_amount = input("🧾 Nouveau montant restant dû (laisser vide pour ne pas changer) : ")
        signed = input("🔐 Signé ? (oui/non, laisser vide pour ne pas changer) : ")
        return client, commercial_id, total_amount, remaining_amount, signed

    def print_delete_contract_view(self, contracts):
        """Affiche la liste des contrats et demande l'ID du contrat à supprimer."""
        self.main_view.print_welcome_message()
        print("\n📋 Liste des contrats 📋 :")
        for contract in contracts:
            print(f"🔹 Contrat ID       : {contract.id}")
            print(f"🧾 Client           : {contract.client.name if contract.client else 'Inconnu'}")
            print(f"💰 Montant total    : {contract.total_amount} €")
            print(
                f"💼 Commercial       : {contract.contact_commercial.email if contract.contact_commercial else 'N/A'}"
            )
            print(f"🧾 Restant dû       : {contract.remaining_amount} €")
            print(f"📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
            print(f"🔐 Signé            : {'Oui' if contract.signed else 'Non'}")
            print("-" * 50)
        choice = input("🗑️ Veuillez entrer l'ID du contrat à supprimer : ")
        return int(choice)
