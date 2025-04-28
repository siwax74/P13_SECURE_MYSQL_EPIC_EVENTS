from datetime import datetime
import time
import sentry_sdk
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.tokens import ObtainToken, RefreshToken


class Decorator:

    @staticmethod
    def with_banner(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.base_view.print_banner()
            return func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def safe_execution(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                if hasattr(self, "authenticated_user"):
                    token_manager = ObtainToken(self.session, self.authenticated_user)
                    stored_token = token_manager.get_stored_tokens()

                    if stored_token:
                        expires_at = datetime.fromisoformat(stored_token["expires_at"])
                        if expires_at < datetime.now():
                            print("\n🔄 Token expiré, tentative de rafraîchissement...")
                            refresh_manager = RefreshToken(
                                self.session, self.authenticated_user, stored_token["refresh_token"]
                            )
                            refresh_manager.update_token()
                    else:
                        print("\n❌ Aucun token trouvé, création d'un nouveau...")
                        token_manager.create_tokens()

                result = func(self, *args, **kwargs)
                if result is None:
                    time.sleep(1)
                return result

            except KeyboardInterrupt:
                print("\n🛑 Interruption du programme.")
            except SQLAlchemyError as e:
                print(f"⚠️ Erreur SQLAlchemy : {e}")
                self.session.rollback()
                sentry_sdk.capture_exception(e)
                time.sleep(2)
            except Exception as e:
                print(f"\n❌ Erreur : {str(e)}")
                sentry_sdk.capture_exception(e)
                time.sleep(2)

        return wrapper
