import graphene
from django.contrib.auth import get_user_model
from .types import UserType
from ..permissions import IsAuthenticated, AllowAny
from .decorators import permission_required

class AccountQueries(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    @permission_required([IsAuthenticated])
    def resolve_me(self, info, **kwargs):
        return info.context.user

    @permission_required([IsAuthenticated])
    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()