import graphene

from Inventory import utils as inventoryUtils
from ..ObjectTypes import HostType, GroupType, VarType, RoleType

class HostInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    groups = graphene.List(graphene.NonNull(graphene.String))
    roles = graphene.List(graphene.NonNull(graphene.String))

class HostMutation(graphene.Mutation):
    class Arguments:
        data = HostInput(required=True)

    host = graphene.Field(HostType)

    def mutate(self, info, name, group):
        host = inventoryUtils.create_host(name, group)
        return HostMutation(host=None)