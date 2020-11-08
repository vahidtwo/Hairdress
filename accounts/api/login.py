import logging
from datetime import datetime

from rest_framework.views import APIView
from unidecode import unidecode

from accounts.models import User
from accounts.serializer import UserSerializer
from core.http import JsonResponse

logger = logging.getLogger('accounts')


class LoginAPI(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        try:
            username = unidecode(str(request.data['username']))
            password = unidecode(str(request.data['password']))
            user = User.objects.get(username=username)
            if not user.password:
                user.set_password(str(user.mobile_number))
                user.save()
            if user.check_password(password):
                user.last_login = datetime.now()
                user.save()
                return JsonResponse(data=UserSerializer(user).data)
            raise User.DoesNotExist
        except User.DoesNotExist:
            return JsonResponse(message='نام کاربری یا رمزعبور اشتباه است', status=404)
        except Exception as e:
            logger.error(f'msg:{str(e)} lg:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
