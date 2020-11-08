import logging
from datetime import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.http import JsonResponse

logger = logging.getLogger('accounts')


class LogOut(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        try:
            Token.objects.get(user=request.user).delete()
            request.user.last_login = datetime.now()
            request.user.save()
            return JsonResponse(message='با موفقیت خارج شدید')
        except Exception as e:
            logger.error(f'msg:{str(e)} lg:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
