# Django Test Projesi


## Proje Hakkında

Kullanıcı hesapları ve kimlik doğrulama işlemlerini GraphQL API üzerinden sunmak için tasarlanmış bir projedir. JWT (JSON Web Tokens) kullanarak güvenli kimlik doğrulama sağlar ve izin sistemi ile hangi kullanıcıların hangi işlemleri yapabileceğini kontrol eder.

## Özellikler

- **JWT Tabanlı Kimlik Doğrulama**: Kullanıcı girişi için token tabanlı güvenli kimlik doğrulama
- **GraphQL API**: GraphQL endpoint'i ile arayüz üzerinden veri sorgulama imkanı
- **İzin Sistemi**: Kullanıcı yetkilendirmesi için izin sistemi
- **CORS Desteği**: Cross-Origin Resource Sharing için güvenlik yapılandırması
- **Test Kapsamı**: Tüm temel işlevler için test kapsama alanı

## Kurulum

Projeyi localinizde çalıştırmak için:

```bash
# 1. Projeyi klonlayın
git clone https://github.com/mehmetakifkucukkaya/django-test.git
cd django_test

# 2. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 3. Migrasyonlarını uygulayın
python manage.py migrate

# 4. Sunucuyu başlatın
python manage.py runserver
```

## API Kullanımı

GraphQL API'sini `http://localhost:8000/graphql/` adresinde bulabilirsiniz. GraphiQL arayüzü ile etkileşimli olarak API'yi keşfedebilirsiniz.

### Örnek Sorgular

**Kullanıcı Kaydı**
```graphql
mutation register{
  createUser(
    username: "test",
    email: "tes@example.com",
    password: "123456"
  ) {
    success
    errors
  }
}
```

**Giriş Yapma ve Token Alma**
```graphql
mutation login{
  tokenAuth(
    email: "tes@example.com",
    password: "123456"
  ) {
    token
  }
}
```

**Profil Bilgilerini Görüntüleme (Kimlik Doğrulama Gerektirir)**
```graphql
query me{
  me {
    id
    username
    email
  }
}
```

> Kimlik doğrulama gerektiren sorgular (me ve getUsers) için Authorization header'ında token göndermelisiniz: `Authorization: Bearer <token>`

### Tüm Kullanıcıları Listeleme (Kimlik Doğrulama Gerektirir)

```graphql
query getUsers{
  users {
    id
    username
    email
    isActive
  }
}
```

## İzin Sistemi

GraphQL çözücülerini (resolver) korumak için bir izin sistemi kullanıldı

- **IsAuthenticated**: Yalnızca giriş yapmış kullanıcıların erişebileceği resolverlar için
- **IsAdminUser**: Yalnızca yönetici kullanıcıların erişebileceği resolverlr için
- **AllowAny**: Herkesin erişebileceği resolverlar için

## Testler

Projenin test kapsamını çalıştırmak için:

```bash
python -m pytest 
```

