import graphene
from django.contrib.auth import get_user_model
import graphql_jwt

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, username, email, password):
        try:
            user = get_user_model()(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
            return CreateUser(success=True)
        except Exception as e:
            return CreateUser(success=False, errors=[str(e)])

class AccountMutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()