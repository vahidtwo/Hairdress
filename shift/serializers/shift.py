from accounts.serializer import UserSerializer
from barber.serializer.barber import BarberSerializer
from barber.serializer.services import ServicesSerializer
from core import serializers
from core.utils.date_time import jalali_datetime
from shift.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True, exclude=('token',))
    barber = BarberSerializer(read_only=True, exclude=('created_at', 'updated_at'))
    start_at = serializers.SerializerMethodField()
    end_at = serializers.SerializerMethodField()
    service = ServicesSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Shift

    def get_start_at(self, obj):
        return jalali_datetime(obj.start_at)

    def get_end_at(self, obj):
        return jalali_datetime(obj.end_at)
