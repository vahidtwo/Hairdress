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

    def get(self, request, barber_id=None):
        try:
            if barber_id:
                return JsonResponse(BarberSerializer(Barber.objects.get(pk=barber_id)).data)
            return JsonResponse(BarberSerializer(Barber.objects.all(), many=True).data)
        except Barber.DoesNotExist:
            return JsonResponse(status=404, message='ارایشگر یافت نشد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def post(self, request):
        try:
            req = request.data
            user = User.objects.get_or_create(username=req['phone_number'], defaults={
                "first_name": req['first_name'],
                "last_name": req['last_name'],
                "phone_number": req['phone_number'],
                "gender": req['gender']
            })
            if user[1]:
                user[0].set_password(req['password'])
                user[0].save()
            barber = Barber.objects.get_or_create(user=user[0])
            if barber[1]:
                return JsonResponse(message='ارایش گر مورد نظر ساخته شد')
            return JsonResponse(status=201, message='ارایش گر مورد نظر موجود است')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def put(self, request, barber_id):
        try:
            req = request.data
            barber = Barber.objects.get(pk=barber_id)
            barber.user.first_name = req['first_name'],
            barber.user.last_name = req['last_name'],
            barber.user.phone_number = req['phone_number'],
            barber.user.username = req['phone_number'],
            barber.user.gender = req['gender']
            barber.user.save()
            return JsonResponse(message='اطلاعات ارایشگر بروز شد')
        except Barber.DoesNotExist:
            return JsonResponse(status=404, message='ارایشگر یافت نشد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
