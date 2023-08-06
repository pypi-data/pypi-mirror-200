from djangoldp.permissions import LDPPermissions


class BookletPermissions(LDPPermissions):

    def get_object_permissions(self, request, view, obj):
        perms = super().get_object_permissions(request, view, obj)
        if request.user in obj.owners.all():
            perms.add('change')
        return perms