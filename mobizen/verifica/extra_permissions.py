from rest_framework.permissions import DjangoModelPermissions, BasePermission

class AuthOnlyModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.add_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    authenticated_users_only = True
    pass
#     def get_required_permissions(self, method, model_cls):
#         pass
# 
#     def has_permission(self, request, view):
#         pass

class IsOwnerOnly(BasePermission):
#     def has_permission(self, request, view):
#         token = request.GET.get('access_token')
#         user = AccessToken.objects.get(token=token)
#         queryset = User.objects.filter(id=user.id)
#         return False
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        try:
            return obj.client.user == request.user
        except:
            return obj.user == request.user        
