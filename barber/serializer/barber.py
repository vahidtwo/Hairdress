from accounts.serializer import UserSerializer
from .services import ServicesSerializer
from barber.models import Barber
from core import serializers


class BarberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    services = ServicesSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Barber
