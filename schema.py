import graphene
from account.graphql.queries import AccountQueries
from account.graphql.mutations import AccountMutations

class Query(AccountQueries, graphene.ObjectType):
    pass

class Mutation(AccountMutations, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
