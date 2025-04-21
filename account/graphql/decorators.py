import functools
from graphql import GraphQLError

def permission_required(permission_classes):
    """
    GraphQL resolver'laı için izin kontrolü yapar.
    Örnek kullanım: @permission_required([IsAuthenticated])
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, info, *args, **kwargs):
            for permission_class in permission_classes:
                permission = permission_class()
                if not permission.has_permission(info):
                    raise GraphQLError(permission.message)
            return func(self, info, *args, **kwargs)
        return wrapper
    return decorator
