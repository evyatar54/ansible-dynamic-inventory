import graphene
from Graphql.ObjectTypes import VarType

class VarInput(graphene.InputObjectType):
    key = graphene.String(required=True)
    value = graphene.String(required=True)

class GroupInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    children = graphene.List(graphene.NonNull(graphene.String))
    roles = graphene.List(graphene.NonNull(graphene.String))
    vars = graphene.List(graphene.NonNull(VarInput))
    isPlatform = graphene.Boolean(required=True)
    enabled = graphene.Boolean(required=True)
