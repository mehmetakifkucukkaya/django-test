class BasePermission:
    """
    Bütün izin sınıflarının temelini oluşturan sınıf.
    """
    message = "Bu işlemi yapmak için izniniz bulunmuyor."

    def has_permission(self, info):
        """
        Kullanıcının bu işlemi yapma izni var mı onu kontrol eden method
        """
        return True


class IsAuthenticated(BasePermission):
    """
    Sadece giriş yapmış kullanıcılar için izin verir.
    """
    message = "Bu işlemi yapabilmek için giriş yapmalısınız."
    
    def has_permission(self, info):
        return info.context.user.is_authenticated


class IsAdminUser(BasePermission):
    """
    Sadece admin kullanıcılar için izin verir.
    """
    message = "Bu işlemi sadece yöneticiler yapabilir."
    
    def has_permission(self, info):
        user = info.context.user
        return user.is_authenticated and user.is_staff


class AllowAny(BasePermission):
    """
    Kimlik doğrulama olmadan herkes için izin verir.
    """
    def has_permission(self, info):
        return True
