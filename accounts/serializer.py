from rest_framework.authtoken.models import Token

from accounts.models import User
from core import serializers


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'username', 'gender', 'token']
    def get_token(self, obj):
        return Token.objects.get_or_create(user=obj)[0].key
