import os
from dotenv import load_dotenv
from app.models.user import User
from app.views.BaseView import BaseView
from app.controllers.main_controller import MainController
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from settings import DATABASE_URL
import sentry_sdk

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("DSN_SENTRY"),
    send_default_pii=True,
)


class LoginController:
    def __init__(self):

        self.views = BaseView()

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
