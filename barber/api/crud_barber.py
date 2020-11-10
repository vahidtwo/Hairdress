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

    def put(self, request, barber_id):
        try:
            req = request.data
            barber = Barber.objects.get(pk=barber_id)
            barber.user.first_name = req['first_name'] if req.get('first_name') else barber.user.first_name
            barber.user.last_name = req['last_name'] if req.get('last_name') else barber.user.last_name
            barber.user.mobile_number = req['mobile_number'] if req.get('mobile_number') else barber.user.mobile_number
            barber.user.gender = req['gender'] if req.get('gender') else barber.user.gender
            barber.user.mobile_number = req['mobile_number'] if req.get('mobile_number') else barber.user.mobile_number
            barber.user.username = req['mobile_number'] if req.get('mobile_number') else barber.user.mobile_number
            barber.user.save()
            return JsonResponse(message='مشخصات ارایشگر بروز شد')
        except Barber.DoesNotExist:
            return JsonResponse(status=404, message='ارایشگر یافت نشد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
