from django.test import Client , TestCase
from django.contrib.auth.models import User

# Create your tests here.

class UserRegTest ( TestCase ) :
    @classmethod
    def setUpTestData ( cls ) :
        cls.user = User.objects.create_user ( username = "userT1" , password = "pwdT1" )

    def test_usert1 ( self ) :
        self.assertEqual ( self.user.username , "userT1" )

# view test

    def test_hongpage ( self ) :
        client = Client ( )
        response = self.client.get ( "" )
        self.assertContains ( response , "Hello Guest !" )

    def test_logon ( self ) :
        client = Client ( )
        response = self.client.force_login ( self.user )
        response = self.client.get ( "" )
        self.assertContains ( response , "Hello userT1 !" )



