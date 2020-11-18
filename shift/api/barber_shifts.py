import datetime
import logging

import pytz
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from barber.models import Barber
from core.http import JsonResponse
from shift.models import Shift
from shift.serializers.shift import ShiftSerializer

logger = logging.getLogger('shift')


class BarberShifts(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, barber_id):
        try:
            barber = Barber.objects.get(pk=barber_id)
            date = datetime.datetime.now().astimezone(pytz.timezone('Asia/Tehran')).replace(
                tzinfo=datetime.timezone.utc)
            shifts = Shift.objects.filter(start_at__gte=date, barber=barber)
            return JsonResponse(ShiftSerializer(shifts, many=True, exclude=('created_at', 'updated_at')).data)
        except Barber.DoesNotExist:
            return JsonResponse(status=404, message='ارایشگر یافت نشد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
