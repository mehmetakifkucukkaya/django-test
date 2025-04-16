import graphene
from django.contrib.auth import get_user_model
from .types import UserType

class AccountQueries(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    @staticmethod
    def resolve_me(root, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None

    @staticmethod
    def resolve_users(root, info, **kwargs):
        if info.context.user.is_authenticated:
            return get_user_model().objects.all()
        return None