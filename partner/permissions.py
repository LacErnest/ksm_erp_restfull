from rest_framework import permissions

# Définition de notre classe IsUserOrReadOnly, précisement une permission 
class IsUserOrReadOnly(permissions.BasePermission):
    """
    Autorisation personnalisée permettant uniquement aux propriétaires d'un objet de le modifier/supprimer.
    """

    def has_object_permission(self, request, view, obj):
        # Les autorisations de lecture sont autorisées pour toute demande,
        # Nous autoriserons donc toujours les demandes GET, HEAD ou OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

class IsSuperUserAndIsAuthenticated(permissions.BasePermission):
    """
    Autorisation personnalisée permettant uniquement aux superuser de lire la liste des users.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )

class DeleteUserPermission(permissions.BasePermission):
    """
    Autorisation empechant la suppression d'un utilisateur
    """
    def has_permission(self, request, view):
        return bool(not request.method == "DELETE")
