import jdatetime
import pytz

from shift.models import WorkShift


def shift_from(date=None):
    if not date:
        now = jdatetime.datetime.now().astimezone(pytz.timezone('Asia/Tehran'))
        if now.minute <= 15:
            now = now.replace(minute=15)
        elif now.minute <= 30:
            now = now.replace(minute=30)
        elif now.minute <= 45:
            now = now.replace(minute=45)
        else:
            now = now.replace(minute=59) + jdatetime.timedelta(minutes=1)
        end_date = now + jdatetime.timedelta(days=7)
        date_ = now
    else:
        date_ = date
        end_date = date + jdatetime.timedelta(days=1)
    work_shift = WorkShift.objects.first()
    usual_day_start_morning = work_shift.usual_day_start_morning
    usual_day_start_morning = jdatetime.time(hour=usual_day_start_morning.hour, minute=usual_day_start_morning.minute)
    usual_day_start_afternoon = work_shift.usual_day_start_afternoon
    usual_day_start_afternoon = jdatetime.time(hour=usual_day_start_afternoon.hour,
                                               minute=usual_day_start_afternoon.minute)
    usual_day_end_morning = work_shift.usual_day_end_morning
    usual_day_end_morning = jdatetime.time(hour=usual_day_end_morning.hour, minute=usual_day_end_morning.minute)
    usual_day_end_afternoon = work_shift.usual_day_end_afternoon
    usual_day_end_afternoon = jdatetime.time(hour=usual_day_end_afternoon.hour, minute=usual_day_end_afternoon.minute)
    shifts = []
    last_shift = date_
    while last_shift <= end_date:
        if usual_day_start_morning <= last_shift.time() < usual_day_end_morning or \
                usual_day_start_afternoon <= last_shift.time() < usual_day_end_afternoon:
            shifts.append(last_shift.replace(second=0, microsecond=0).togregorian())
        last_shift = last_shift + jdatetime.timedelta(minutes=15)
    return shifts
