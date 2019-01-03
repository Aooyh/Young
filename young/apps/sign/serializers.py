import re

from apps.users.models import User

from rest_framework import serializers


def check_mobile(mobile):
    if re.match('1[357896]\d{9}$', mobile):
        return True


class UserRegisterSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(max_length=4, min_length=4, label='短信验证码', write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'mobile', 'sms_code']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        username = attrs.get('username')
        password = attrs.get('password')
        if not check_mobile(mobile):
            raise serializers.ValidationError
        if not re.match('\w{6,12}$', username):
            raise serializers.ValidationError
        if not re.match('.{8,12}$', password):
            raise serializers.ValidationError
        return attrs

    def create(self, validated_data):
        validated_data.pop('sms_code')
        password = validated_data.pop('password')
        new_user = User.objects.create(**validated_data)
        new_user.set_password(password)
        new_user.nickname = validated_data['username']
        new_user.save()
        return new_user
