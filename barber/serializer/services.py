from barber.models import Service
from core import serializers


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'price_per_15_min')
        model = Service
