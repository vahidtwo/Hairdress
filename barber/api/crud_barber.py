import logging

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from accounts.models import User
from barber.models import Barber
from barber.serializer.barber import BarberSerializer
from core.http import JsonResponse

logger = logging.getLogger('barber')


class CRUDBarber(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        try:
            return JsonResponse(BarberSerializer(Barber.objects.all(), many=True).data)
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def post(self, request):
        try:
            req = request.data
            user = User.objects.get_or_create(username=req['mobile_number'], defaults={
                "first_name": req['first_name'],
                "last_name": req['last_name'],
                "mobile_number": req['mobile_number'],
                "gender": req['gender']
            })
            Barber.objects.create(user=user[0])
            if user[1]:
                return JsonResponse(message='ارایش گر مورد نظر ساخته شد')
            return JsonResponse(message='ارایش گر مورد نظر موجود است')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
