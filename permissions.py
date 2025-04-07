class BasePermissions:
    def __init__(self, authenticated_user):
        self.authenticated_user = authenticated_user
        self.roles = {
            "commercial": self.authenticated_user.is_commercial,
            "management": self.authenticated_user.is_management,
            "support": self.authenticated_user.is_support,
        }

    @property
    def is_commercial(self):
        return self.roles.get("commercial", False)

    @property
    def is_management(self):
        return self.roles.get("management", False)

    @property
    def is_support(self):
        return self.roles.get("support", False)

    def has_permission(self, permission_type):
        return self.roles.get(permission_type, False)

    def get_available_permissions(self):
        return [role for role, has_permission in self.roles.items() if has_permission]
