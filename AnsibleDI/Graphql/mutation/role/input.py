import graphene

class CreateRoleInput(graphene.InputObjectType):
    name = graphene.String(required=True)