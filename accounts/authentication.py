from accounts.models import Token, User

class PasswordlessAuthenticationBackend(object):

    def authenticate(self, uid):
        # print('\n\nauth\n\n+++++\n')
        try:
            token = Token.objects.get(uid = uid)
        except Token.DoesNotExist:
            return None
        try:
            return User.objects.get(email = token.email)
        except User.DoesNotExist:
            return User.objects.create(email = token.email)

    def get_user(self, email):
        try:
            return User.objects.get(email = email)
        except User.DoesNotExist:
            return None
