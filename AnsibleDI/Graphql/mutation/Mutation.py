import graphene
from .Host import HostMutation

class Mutation(graphene.ObjectType):
    create_host = HostMutation.Field()
    