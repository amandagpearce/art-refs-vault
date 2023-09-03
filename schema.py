import graphene


class UserType(graphene.ObjectType):
    # Define user fields here
    pass


class Query(graphene.ObjectType):
    # Define queries here
    pass


class Mutation(graphene.ObjectType):
    # Define mutations here
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
