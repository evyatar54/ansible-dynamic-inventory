import graphene
from django.db import transaction
from .input import GroupInput
from Inventory import utils as inventoryUtils
from Graphql.ObjectTypes import GroupType

class CreateGroupMutation(graphene.Mutation):
    class Arguments:
        data = GroupInput(required=True)

    group = graphene.Field(GroupType)

    def mutate(self, info, data=None):
        group = inventoryUtils.create_group(
            data["name"],
            data["children"],
            data["roles"],
            data["vars"],
            data["isPlatform"],
            data["enabled"]
            )
        return CreateGroupMutation(group=group)

class DeleteGroupMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    id = graphene.Field(graphene.String)

    def mutate(self, info, name):
        group = inventoryUtils.get_group(name)
        id = group.id
        group.delete()
        return DeleteGroupMutation(id=id)

class UpdateGroupMutation(graphene.Mutation):
    class Arguments:
        data = graphene.NonNull(GroupInput)

    group = graphene.Field(GroupType)

    def mutate(self, info, data):
        with transaction.atomic():
            group = inventoryUtils.update_group(
                data["name"],
                data["children"],
                data["roles"],
                data["vars"],
                data["isPlatform"],
                data["enabled"]
            )
        return UpdateGroupMutation(group=group)