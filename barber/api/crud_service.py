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
            service = Service.objects.get_or_create(name=request.data['name'],
                                                    price_per_15_min=request.data['price_per_15_min'])
            if not service[1]:
                return JsonResponse(message='سرویس مورد موجود است')
            return JsonResponse(status=201, message='سرویس مورد نظر اضافه شد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def put(self, request, service_id):
        try:
            service = Service.objects.get(pk=service_id)
            service.name = request.data['name'] if request.data.get('name') else service.name
            service.price_per_15_min = request.data['price_per_15_min'] if request.data.get(
                'price_per_15_min') else service.price_per_15_min
            service.save()
            return JsonResponse(message='سرویس مورد نظر بروز شد')
        except Service.DoesNotExist:
            return JsonResponse(status=404, message='سرویس مورد نظر یافت نشد')
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
