import graphene
from django.db import transaction
from .input import HostInput
from Inventory import utils as inventoryUtils
from Graphql.ObjectTypes import HostType

class CreateHostMutation(graphene.Mutation):
    class Arguments:
        data = HostInput(required=True)

    host = graphene.Field(HostType)

    def mutate(self, info, data=None):
        host = inventoryUtils.create_host(**data)
        return CreateHostMutation(host=host)

class DeleteHostMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    id = graphene.Field(graphene.String)

    def mutate(self, info, name):
        host = inventoryUtils.get_host(name)
        id = host.id
        host.delete()
        return DeleteHostMutation(id=id)

class UpdateHostMutation(graphene.Mutation):
    class Arguments:
        data = graphene.NonNull(HostInput)

    host = graphene.Field(HostType)

    def mutate(self, info, data):
        with transaction.atomic():
            host = inventoryUtils.update_host(
                data["name"],
                data["groups"],
                data["roles"]
            )
        return UpdateHostMutation(host=host)