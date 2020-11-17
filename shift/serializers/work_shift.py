from core import serializers
from shift.models import WorkShift


class WorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = WorkShift
