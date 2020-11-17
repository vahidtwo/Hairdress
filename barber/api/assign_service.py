import logging

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from barber.models import Barber, Service
from core.http import JsonResponse

logger = logging.getLogger('barber')


class AssignService(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        try:
            req = request.data
            barber = Barber.objects.get(pk=req['barber_id'])
            services = Service.objects.filter(pk__in=req['service_ids'])
            for service in services:
                barber.services.add(service)
            return JsonResponse(status=201, message='سرویس مورد نظر به ارایشگر اضافه شد')
        except Barber.DoesNotExist:
            return JsonResponse(status=404, message='ارایشگر یافت نشد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def delete(self, request):
        try:
            req = request.data
            barber = Barber.objects.get(pk=req['barber_id'])
            services = Service.objects.filter(pk__in=req['service_ids'])
            for service in services:
                barber.services.remove(service)
            return JsonResponse(message='سرویس مورد نظر از ارایشگر حذف شد')
        except Barber.DoesNotExist:
            return JsonResponse(status=404, message='ارایشگر یافت نشد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
