#######################################################################################################################
#                                                    CONTRATS                                                         #
#######################################################################################################################
class ContractView:
    def __init__(self, main_view):
        self.main_view = main_view

    def print_contract_menu(self):
        self.main_view.print_welcome_message()
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
            print(f"🔹 Contrat ID       : {contract.id}")
            print(
                f"🧾 Client           : {contract.client_information.name if contract.client_information else 'Inconnu'}"
            )
            print(f"💰 Montant total    : {contract.total_amount} €")
            print(
                f"💼 Commercial       : {contract.contact_commercial.email if contract.contact_commercial else 'N/A'}"
            )
            print(f"🧾 Restant dû       : {contract.remaining_amount} €")
            print(f"📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
            print(f"🔐 Signé            : {'Oui' if contract.signed else 'Non'}")
            print("-" * 50)
            print("4️⃣ - Retour au menu principal")
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
            print(f"🔹 Contrat ID       : {contract.id}")
            print(f"🧾 Client           : {contract.client_information if contract.client_information else 'Inconnu'}")
            print(f"💰 Montant total    : {contract.total_amount} €")
            print(f"💼 Commercial       : {contract.contact_commercial if contract.contact_commercial else 'N/A'}")
            print(f"🧾 Restant dû       : {contract.remaining_amount} €")
            print(f"📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
            print(f"🔐 Signé            : {'Oui' if contract.signed else 'Non'}")
            print("-" * 50)
            print("4️⃣ - Retour au menu principal")
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
            print(f"🔹 Contrat ID       : {contract.id}")
            print(f"🧾 Client           : {contract.client_information if contract.client_information else 'Inconnu'}")
            print(f"💰 Montant total    : {contract.total_amount} €")
            print(f"💼 Commercial       : {contract.contact_commercial if contract.contact_commercial else 'N/A'}")
            print(f"🧾 Restant dû       : {contract.remaining_amount} €")
            print(f"📅 Date de création : {contract.created_at.strftime('%d/%m/%Y')}")
            print(f"🔐 Signé            : {'Oui' if contract.signed else 'Non'}")
            print("-" * 50)
            print("🔙 4 - Retour au menu principal")
        choice = input("Veuillez entrez l'id du contrat a supprimer: ")
        return int(choice)
