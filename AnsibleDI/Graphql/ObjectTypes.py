from graphene_django import DjangoObjectType
from Inventory.models import Host, Group, Role, Var

class HostType(DjangoObjectType):
    class Meta:
        model = Host
        fields = ("id", "name", "groups", "roles")

class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = ("id", "name", "children", "roles", "vars", "isPlatform", "enabled")

class RoleType(DjangoObjectType):
    class Meta:
        model = Role
        fields = ("id", "name")

class VarType(DjangoObjectType):
    class Meta:
        model = Var
        fields = ("id", "group", "key", "value")