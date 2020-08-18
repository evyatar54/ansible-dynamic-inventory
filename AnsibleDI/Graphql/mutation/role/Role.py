import graphene

from .input import CreateRoleInput
from Inventory import utils as inventoryUtils
from Graphql.ObjectTypes import RoleType

class CreateRoleMutation(graphene.Mutation):
    class Arguments:
        data = CreateRoleInput(required=True)

    role = graphene.Field(RoleType)

    def mutate(self, info, data=None):
        role = inventoryUtils.create_role(data["name"])
        return CreateRoleMutation(role=role)

class DeleteRoleMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    id = graphene.Field(graphene.String)

    def mutate(self, info, name):
        role = inventoryUtils.get_role(name)
        id = role.id
        role.delete()
        return DeleteRoleMutation(id=id)