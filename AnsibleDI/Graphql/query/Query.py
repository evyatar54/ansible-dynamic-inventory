import graphene
from ..ObjectTypes import GroupType, HostType, VarType, RoleType
from Inventory import utils as inventoryUtils

class Query(graphene.ObjectType):
    hosts = graphene.List(HostType)

    groups = graphene.List(GroupType)

    roles = graphene.List(RoleType)


    def resolve_hosts(root, info):
        return inventoryUtils.get_all_hosts()

    def resolve_groups(root, info):
        return inventoryUtils.get_all_groups()

    def resolve_roles(root, info):
        return inventoryUtils.get_all_roles()