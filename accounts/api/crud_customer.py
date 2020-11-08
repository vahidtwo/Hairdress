import logging

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializer import UserSerializer
from core.http import JsonResponse

logger = logging.getLogger('accounts')


class CRUDCustomer(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, user_id=None):
        try:
            if user_id:
                user = User.objects.get(pk=user_id)
            else:
                user = User.objects.filter(barber__isnull=True)
            return JsonResponse(UserSerializer(user, many=True).datao)
        except User.DoesNotExist:
            return JsonResponse(status=404, message='مشتری یافت نشد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def post(self, request):
        try:
            req = request.data
            User.objects.get_or_create(username=req['mobile_number'], defaults={
                "gender": req['gender'] if req.get('gender') else False,
                "mobile_number": req['mobile_number'],
                "username": req['mobile_number'],
                'first_name': req['first_name'],
                'last_name': req['last_name'],
            })
            return JsonResponse(message='مشتری با موفقیت ساخته شد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def put(self, request, user_id):
        try:
            req = request.data
            user = User.objects.get(pk=user_id)
            user.mobile_number = req['mobile_number'],
            user.username = req['mobile_number'],
            user.first_name = req['first_name'],
            user.last_name = req['last_name'],
            user.save()
            return JsonResponse(message='مشتری با موفقیت بروز رسانی شد')
        except User.DoesNotExist:
            return JsonResponse(message='مشتری یافت نشد', status=404)
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
