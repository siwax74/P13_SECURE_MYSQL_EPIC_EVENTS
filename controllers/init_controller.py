import os
from dotenv import load_dotenv
from models.user import User
from views.CLIView import CLIView
from views.main_view import MainView
from controllers.main_controller import MainController
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import bcrypt

load_dotenv()


class CLIController:
    def __init__(self):

        self.views = CLIView()

        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")

        DATABASE_URL = f"mariadb+mariadbconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        self.engine = create_engine(DATABASE_URL, echo=False)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def run(self):
        while True:
            try:
                self.views.print_banner()
                email, password = self.views.print_login_form()
                authenticated_user = self.authenticate_user(email, password)
                if authenticated_user:
                    self.main_controller = MainController(self.session, authenticated_user, self.views)
                    self.main_controller.run()
                else:
                    print("Échec de l'authentification.")

            except KeyboardInterrupt:
                print("\nInterruption du programme.")
                break
            except SQLAlchemyError as e:
                print(f"Erreur SQLAlchemy: {e}")
            except Exception as e:
                print(f"Une erreur est survenue: {e}")

    def authenticate_user(self, email, password):
        """Vérifie si l'utilisateur existe et si le mot de passe est correct."""
        user = self.session.query(User).filter_by(email=email).first()

        if not user:
            print("\n❌ Utilisateur non trouvé.")
            return None
        if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            print("\n✅ Connexion réussie !")
            return user
        else:
            print("\n❌ Mot de passe incorrect.")
            return None
