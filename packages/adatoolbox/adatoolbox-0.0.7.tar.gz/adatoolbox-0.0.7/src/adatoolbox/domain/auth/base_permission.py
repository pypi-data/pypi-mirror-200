from django.core.exceptions import PermissionDenied


class AuthApiPermission:
    def has_permission(self, permission: str, user: dict) -> None:
        if permission not in user.get('permissoes'):
            raise PermissionDenied()