import datetime
import logging

import jdatetime
import pytz
from rest_framework.views import APIView

from barber.models import Barber
from barber.serializer.barber import BarberSerializer
from core.http import JsonResponse
from core.utils.date_time import jalali_datetime, fix_date
from core.utils.paginate import paginate
from core.utils.shift_from import shift_from
from shift.models import Shift

logger = logging.getLogger('shift')


class AvailableShift(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, barber_id):
        try:
            barber = Barber.objects.get(pk=barber_id)
            date = datetime.datetime.now().astimezone(pytz.timezone('Asia/Tehran')).replace(tzinfo=datetime.timezone.utc)
            shifts = Shift.objects.filter(end_at__gte=date, barber=barber)
            if request.query_params.get('date'):
                date = jdatetime.datetime.strptime(fix_date(request.query_params['date']), '%Y/%m/%d')
                shifts = shifts.filter(end_at__lte=date.togregorian() + datetime.timedelta(days=1))
                all_shift_times = shift_from(date)
            else:
                all_shift_times = shift_from()
            for i in shifts:
                start = i.start_at
                end = i.end_at
                delta = (end - start).seconds // 60 // 15
                if delta != 1:
                    times = [start + datetime.timedelta(minutes=z * 15) for z in range(0, delta)]
                else:
                    times = [start]
                for time in times:
                    print(all_shift_times[0], times)
                    all_shift_times.remove(time)
            work_shifts = []
            for i in all_shift_times:
                work_shifts.append({
                    'start_at': jalali_datetime(i),
                    'end_at': jalali_datetime(i + datetime.timedelta(minutes=15))
                })
            return JsonResponse(**paginate(data=work_shifts, limit=50, page=request.query_params.get('page', 1)),
                                extra={"barber": BarberSerializer(barber, exclude=(
                                    'created_at', 'updated_at', 'services')).data})
        except Exception as e:
            logger.error(f'msg:{str(e)}, lo:{e.__traceback__.tb_lineno}')
            return JsonResponse(status=500)
