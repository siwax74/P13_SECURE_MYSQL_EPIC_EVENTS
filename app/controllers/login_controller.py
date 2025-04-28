from datetime import datetime
import os
from app.tokens import ObtainToken, RefreshToken
from app.models.user import User
from app.views.BaseView import BaseView
from app.controllers.main_controller import MainController
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from app.regex import is_valid_email
from settings import DATABASE_URL, DSN_SENTRY
import sentry_sdk
from app.decorators import Decorator

sentry_sdk.init(
    dsn=DSN_SENTRY,
    send_default_pii=True,
)


#######################################################################################################################
#                                                    LOGIN                                                            #
#######################################################################################################################
class LoginController:
    def __init__(self):
        self.base_view = BaseView()
        self.engine = create_engine(DATABASE_URL, echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @Decorator.with_banner
    @Decorator.safe_execution
    def run(self):
        while True:
            email, password = self.base_view.print_login_form()
            authenticated_user = self.authenticate_user(email, password)
            if authenticated_user:
                self.main_controller = MainController(self.session, authenticated_user, self.base_view)
                return self.main_controller.run()

    @Decorator.safe_execution
    def authenticate_user(self, email, password):
        """Vérifie si l'utilisateur existe et si le mot de passe est correct."""
        if not is_valid_email(email):
            print("\n❌ Invalid Email !.")
            return None
        if not password:
            print("\n❌ Invalid Password !.")
            return None

        user = self.session.query(User).filter_by(email=email).first()
        if not user:
            print("\n❌ Utilisateur non trouvé.")
            return None

        if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            token_manager = ObtainToken(self.session, user)
            stored_token = token_manager.get_stored_tokens()
            if stored_token and stored_token.get("user") != email:
                print("\n⚠️ Utilisateur différent détecté, création d'un nouveau token.")
                token_manager.create_tokens()
            elif stored_token:
                if datetime.fromisoformat(stored_token["expires_at"]) < datetime.now():
                    refresh_manager = RefreshToken(self.session, user, stored_token["refresh_token"])
                    refresh_manager.update_token()
                else:
                    print("\n✅ Connexion réussie avec token valide !")
            else:
                token_manager.create_tokens()

            return user
        else:
            print("\n❌ Mot de passe incorrect.")
            return None
