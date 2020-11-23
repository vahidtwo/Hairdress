import logging

from django.core.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializer import UserSerializer
from core.http import JsonResponse
from core.utils.paginate import paginate

logger = logging.getLogger('accounts')


class CRUDCustomer(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, user_id=None):
        try:
            if user_id:
                user = User.objects.get(pk=user_id)
                return JsonResponse(UserSerializer(user).data)
            else:
                user = User.objects.filter(barber__isnull=True)
                return JsonResponse(**paginate(user,
                                               serializer=UserSerializer,
                                               page=request.query_params.get('page'),
                                               limit=request.query_params.get('limit')))
        except User.DoesNotExist:
            return JsonResponse(status=404, message='مشتری یافت نشد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def post(self, request):
        try:
            req = request.data
            user = User.objects.get_or_create(username=req['phone_number'], defaults={
                "gender": req['gender'] if req.get('gender') else False,
                "phone_number": req['phone_number'],
                "username": req['phone_number'],
                'first_name': req['first_name'],
                'last_name': req['last_name'],
            })[0]
            user.set_password(req['password'])
            user.save()
            return JsonResponse(message='مشتری با موفقیت ساخته شد')
        except ValidationError as e:
            return JsonResponse(status=400, message=str(e))
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def put(self, request, user_id):
        try:
            req = request.data
            user = User.objects.get(pk=user_id)
            user.phone_number = req['phone_number'],
            user.username = req['phone_number'],
            user.first_name = req['first_name'],
            user.last_name = req['last_name'],
            user.gender = req['gender'],
            user.save()
            return JsonResponse(message='مشتری با موفقیت بروز رسانی شد')
        except User.DoesNotExist:
            return JsonResponse(message='مشتری یافت نشد', status=404)
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
