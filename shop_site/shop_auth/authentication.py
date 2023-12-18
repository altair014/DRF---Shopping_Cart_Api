from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework.exceptions import AuthenticationFailed

class CustomBaseAuthentication(BaseAuthentication):
    def authenticate(self, request, userid=None, password=None, **kwargs):
        print(userid)
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('User do not exist.')
        else:
            if user.check_password(password):
                return (user, None)

        # print(username)
        # print(password)
           
        # if username is None: 
        #     return None 
        # try: 
        #     user = User.objects.get(email=username)
        #     print(user) 
        # except User.DoesNotExist: 
        #     raise AuthenticationFailed('User do not exist.')   
        # return (user, None)
