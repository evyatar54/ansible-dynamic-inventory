import graphene

class HostInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    groups = graphene.List(graphene.NonNull(graphene.String))
    roles = graphene.List(graphene.NonNull(graphene.String))