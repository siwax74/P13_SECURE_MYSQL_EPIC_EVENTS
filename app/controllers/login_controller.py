import os
from app.models.user import User
from app.views.BaseView import BaseView
from app.controllers.main_controller import MainController
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
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

    ############################################### MENU LOGIN ########################################################
    @Decorator.with_banner
    @Decorator.safe_execution
    def run(self):
        while True:
            email, password = self.base_view.print_login_form()
            authenticated_user = self.authenticate_user(email, password)
            if authenticated_user:
                self.main_controller = MainController(self.session, authenticated_user, self.base_view)
                return self.main_controller.run()

    ############################################### AUTHENTICATE USER #################################################
    @Decorator.safe_execution
    def authenticate_user(self, email, password):
        """Vérifie si l'utilisateur existe et si le mot de passe est correct."""
        if not email:
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
            print("\n✅ Connexion réussie !")
            return user
        else:
            print("\n❌ Mot de passe incorrect.")
            return None
