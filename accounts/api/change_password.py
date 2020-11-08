import logging

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from unidecode import unidecode

from core.http import JsonResponse

logger = logging.getLogger('accounts')


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        try:
            password = unidecode(str(request.data['password']))
            request.user.set_password(password)
            request.user.save()
            return JsonResponse(message='با موفقیت پسورد شما عوض شد')
        except Exception as e:
            logger.error(f'msg:{str(e)} lg:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
