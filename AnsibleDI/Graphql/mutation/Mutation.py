import graphene
from .host.Host import CreateHostMutation, DeleteHostMutation, UpdateHostMutation
from .group.Group import CreateGroupMutation, DeleteGroupMutation, UpdateGroupMutation
from .role.Role import CreateRoleMutation, DeleteRoleMutation

class Mutation(graphene.ObjectType):
    create_host = CreateHostMutation.Field()
    update_host = UpdateHostMutation.Field()
    delete_host = DeleteHostMutation.Field()

    create_group = CreateGroupMutation.Field()
    update_group = UpdateGroupMutation.Field()
    delete_group = DeleteGroupMutation.Field()

    create_role = CreateRoleMutation.Field()
    delete_role = DeleteRoleMutation.Field()
    