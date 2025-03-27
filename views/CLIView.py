from termcolor import colored
import getpass


class CLIView:
    CLI_VERSION = "0.0.1"
    AUTHOR = "Siwax74"
    COPYRIGHT = "2025 Epic_Events"

    def print_banner(self):
        banner = r"""
  ______ _____ _____ _____   ________      ________ _   _ _______ _____  
 |  ____|  __ \_   _/ ____| |  ____\ \    / /  ____| \ | |__   __/ ____| 
 | |__  | |__) || || |      | |__   \ \  / /| |__  |  \| |  | | | (___   
 |  __| |  ___/ | || |      |  __|   \ \/ / |  __| | . ` |  | |  \___ \  
 | |____| |    _| || |____  | |____   \  /  | |____| |\  |  | |  ____) | 
 |______|_|   |_____\_____| |______|   \/   |______|_| \_|  |_| |_____/  
                        ______                                           
                       |______| Epic_Events - Secure and optimised MySQL BDD
        """
        print(colored(banner, "cyan"))
        # Utilisation de `self` pour accéder aux variables de classe
        print(colored(f"ClI Version: {self.CLI_VERSION}", "yellow"))
        print(colored(f"Made by {self.AUTHOR}", "yellow"))
        print(colored(self.COPYRIGHT, "yellow"))

    def print_login_form(self):
        print("=== Connexion ===")
        email = input("Email: ")
        password = getpass.getpass("Mot de passe: ")  # Masque le mot de passe pour plus de sécurité
        return email, password
