import graphene
from Graphql.query.Query import Query
from Graphql.mutation.Mutation import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)