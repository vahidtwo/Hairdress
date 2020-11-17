from accounts.serializer import UserSerializer
from barber.models import Barber
from core import serializers
from .services import ServicesSerializer


class BarberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, exclude=('token',))
    services = ServicesSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Barber
