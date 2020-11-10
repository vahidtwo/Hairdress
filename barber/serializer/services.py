from barber.models import Service
from core import serializers


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        model = Service
