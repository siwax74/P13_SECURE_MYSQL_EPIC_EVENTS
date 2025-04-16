from functools import wraps
import time


class BasePermissions:
    """Gère les rôles et permissions de l'utilisateur connecté."""

    def __init__(self, authenticated_user):
        self.authenticated_user = authenticated_user

    @staticmethod
    def check_permission(*allowed_roles):
        """
        Décorateur pour restreindre l'accès à une méthode selon les rôles autorisés.
        Exemple : @check_permission("is_commercial", "is_support")
        """

        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if not any(getattr(self.authenticated_user, role, False) for role in allowed_roles):
                    print("❌ Permission refusée. Accès non autorisé.")
                    time.sleep(1)
                    return None
                return func(self, *args, **kwargs)

            return wrapper

        return decorator
