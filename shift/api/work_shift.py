import logging

import jdatetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from core.http import JsonResponse
from shift.models import WorkShift
from shift.serializers import WorkShiftSerializer

logger = logging.getLogger('shift')


class WorkShiftAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        try:
            time_format = '%H:%M:%S'
            req = request.data
            WorkShift.objects.all().delete()
            WorkShift.objects.create(
                usual_day_start_morning=jdatetime.datetime.strptime(req['usual_day_start_morning'],
                                                                    time_format).togregorian().time(),
                usual_day_end_morning=jdatetime.datetime.strptime(req['usual_day_end_morning'],
                                                                  time_format).togregorian().time(),
                usual_day_start_afternoon=jdatetime.datetime.strptime(req['usual_day_start_afternoon'],
                                                                      time_format).togregorian().time(),
                usual_day_end_afternoon=jdatetime.datetime.strptime(req['usual_day_end_afternoon'],
                                                                    time_format).togregorian().time())
            return JsonResponse(status=201, message='ساعت کاری ارایشگاه با موفقیت ساخته شد')
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)

    def get(self, request):
        try:
            return JsonResponse(WorkShiftSerializer(WorkShift.objects.first()).data)
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
