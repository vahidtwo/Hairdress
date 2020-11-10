import logging

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from barber.models import Service
from barber.serializer.services import ServicesSerializer
from core.http import JsonResponse

logger = logging.getLogger('barber')


class CRUDService(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, barber_id=None):
        try:
            if barber_id:
                services = Service.objects.filter(barber_id=barber_id)
            else:
                services = Service.objects.all()
            return JsonResponse(ServicesSerializer(services, many=True).data)
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def post(self, request):
        try:
            Service.objects.create(name=request.data['name'])
            return JsonResponse(message='سرویس مورد نظر اضافه شد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def delete(self, request, service_id):
        try:
            Service.objects.get(pk=service_id).delete()
            return JsonResponse(message='سرویس مورد نظر حذف شد')
        except Service.DoesNotExist:
            return JsonResponse(message='سرویس مورد نظر موجود نیست', status=404)
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
