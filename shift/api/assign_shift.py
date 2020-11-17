import logging

import jdatetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import User
from barber.models import Barber, Service
from core.http import JsonResponse
from shift.models import Shift

logger = logging.getLogger('shift')


class AssignShift(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        try:
            req = request.data
            customer = User.objects.get(pk=req['customer_id'])
            barber = Barber.objects.get(pk=req['barber_id'])
            start_at = jdatetime.datetime.strptime(req['start_at'], '%Y/%m/%d %H:%M:%S').togregorian()
            end_at = jdatetime.datetime.strptime(req['end_at'], '%Y/%m/%d %H:%M:%S').togregorian()
            service = Service.objects.get(pk=req['service_id'])
            Shift.objects.create(barber=barber, customer=customer, start_at=start_at, end_at=end_at, service=service)
            return JsonResponse(message='نوبت دهی با موفقیت ثبت شد')
        except ValueError as e:
            return JsonResponse(status=400, message=str(e))
        except Service.DoesNotExist:
            return JsonResponse(message='سرویس یافت نشد', status=404)
        except User.DoesNotExist:
            return JsonResponse(message='مشتری یافت نشد', status=404)
        except Barber.DoesNotExist:
            return JsonResponse(message='ارایشگر یافت نشد', status=404)
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
