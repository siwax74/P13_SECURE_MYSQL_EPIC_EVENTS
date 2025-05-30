from termcolor import colored
import getpass


class BaseView:

    CLI_VERSION = "1.0.0"
    AUTHOR = "Siwax74"
    COPYRIGHT = "2025 Epic_Events"

    def print_banner(self):
        banner = r"""
  ______ _____ _____ _____   ________      ________ _   _ _______ _____   
 |  ____|  __ \_   _/ ____| |  ____\ \    / /  ____| \ | |__   __/ ____/
 | |__  | |__) || || |      | |__   \ \  / /| |__  |  \| |  | | | (___   
 |  __| |  ___/ | || |      |  __|   \ \/ / |  __| | . ` |  | |  \___ \  
 | |____| |    _| || |____  | |____   \  /  | |____| |\  |  | |  ____) /
 |______|_|   |_____\_____| |______|   \/   |______|_| \_|  |_| |_____/  
                       |______| Epic_Events - Secure and optimised MySQL BDD
        """
        print(colored(banner, "cyan"))
        print(colored(f"ClI Version: {self.CLI_VERSION}", "yellow"))
        print(colored(f"Made by {self.AUTHOR}", "yellow"))
        print(colored(self.COPYRIGHT, "yellow"))

    def print_login_form(self):
        print("=== Connexion ===")
        email = input("Email: ")
        password = getpass.getpass("Mot de passe: ")
        return email, password

    def print_logout_view(self):
        print("\n⚠️  Vous êtes sur le point de vous déconnecter.")
        choice = input("Êtes-vous sûr de vouloir vous déconnecter ? (y/n): ").lower()
        return choice
