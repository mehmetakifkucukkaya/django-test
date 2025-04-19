import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from graphene_django.utils.testing import GraphQLTestCase
import json

# Test için ortak veri
TEST_USER = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'testpass123'
}

@pytest.mark.django_db
class TestAccount(GraphQLTestCase):
    
    #* Her test öncesi otomatik oalrak çalışır. User modelini her testte ayrı ayrı çağırmaya gerek kalmıyor.
    def setUp(self):
        self.User = get_user_model()
    
    # Model Testleri
    
    #* Yeni kullanıcı oluşturma
    def test_create_user(self):
        user = self.User.objects.create_user(**TEST_USER)
        assert user.email == TEST_USER['email']
        assert user.username == TEST_USER['username']
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    #* Aynı mail ile kullanıcı oluşturma

    def test_email_is_unique(self):
        self.User.objects.create_user(**TEST_USER)
        with pytest.raises(IntegrityError):
            self.User.objects.create_user(
                username="another",
                email=TEST_USER['email'],
                password="pass123"
            )

    # GraphQL Mutation Testleri
    
    def test_user_creation_flow(self):
        #* GraphQL üzerinden kullanıcı oluşturuyorz
        
        mutation = '''
            mutation {
                createUser(
                    email: "test@example.com",
                    username: "testuser",
                    password: "testpass123"
                ) {
                    success
                    errors
                }
            }
        '''
        response = self.client.post('/graphql/', {'query': mutation})
        
        #* GraphQL yanıtını kontrol ediyoruz
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['data']['createUser']['success'],
            True
        )

        #* Oluşturulan kullanıcının model verilerini kontrol edelim
        user = self.User.objects.get(email="test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
    #* Token kontrol testi
    def test_token_auth(self):
        #* Kullanıcı oluşturutyor ve token alıyor
        self.User.objects.create_user(**TEST_USER)
        mutation = '''
            mutation {
                tokenAuth(email: "test@example.com", password: "testpass123") {
                    token
                }
            }
        '''
        response = self.client.post('/graphql/', {'query': mutation})
        self.assertIn('token', json.loads(response.content)['data']['tokenAuth'])
        

    # GraphQL Query Testleri
    
    #* Me işlemini test eder (Kullnaıcı girişi yapılmamış halde)
    def test_me_query_unauthenticated(self):
        query = '''
            query { me { id email username } }
        '''
        response = self.client.post('/graphql/', {'query': query})
        self.assertIsNone(json.loads(response.content)['data']['me'])


    #* Me işlemini test eder (Kullnaıcı girişi yapılmış halde)
    def test_me_query_authenticated(self):
        # Kullanıcı oluştur ve token al
        user = self.User.objects.create_user(**TEST_USER)
        mutation = '''
            mutation {
                tokenAuth(email: "test@example.com", password: "testpass123") {
                    token
                }
            }
        '''
        response = self.client.post('/graphql/', {'query': mutation})
        token = json.loads(response.content)['data']['tokenAuth']['token']

        # Me query'si çalıştır
        query = '''
            query { me { id email username } }
        '''
        response = self.client.post(
            '/graphql/',
            {'query': query},
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        data = json.loads(response.content)['data']['me']
        self.assertEqual(data['email'], TEST_USER['email'])
        self.assertEqual(data['username'], TEST_USER['username'])

    #* Users listesini test eder (Kullnaıcı girişi yapılmamış halde)
    def test_users_query_unauthenticated(self):
        query = '''
            query { users { id email username } }
        '''
        response = self.client.post('/graphql/', {'query': query})
        self.assertIsNone(json.loads(response.content)['data']['users'])

    #* Users listesini test eder (Kullnaıcı girişi yapılmış halde)
    def test_users_query_authenticated(self):
        #* Test için iki kullanıcı oluşturuluyor
        self.User.objects.create_user(**TEST_USER)
        self.User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpass123"
        )

        
        mutation = '''
            mutation {
                tokenAuth(email: "test@example.com", password: "testpass123") {
                    token
                }
            }
        '''
        response = self.client.post('/graphql/', {'query': mutation})
        token = json.loads(response.content)['data']['tokenAuth']['token']

        
        query = '''
            query { 
                users { 
                    id 
                    email 
                    username 
                } 
            }
        '''
        response = self.client.post(
            '/graphql/',
            {'query': query},
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        data = json.loads(response.content)['data']['users']
        
        #* Kontrol kısmı
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)  # 2 kullanıcı oluşturduk
        self.assertEqual(data[0]['email'], TEST_USER['email'])
        self.assertEqual(data[1]['email'], "test2@example.com")
