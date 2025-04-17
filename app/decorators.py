import time
import sentry_sdk
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


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
