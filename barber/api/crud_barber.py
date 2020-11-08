import logging

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

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
