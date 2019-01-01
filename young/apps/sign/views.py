import random

from apps.users.models import User
from celery_tasks.sms.tasks import send_sms_code
from .serializers import UserRegisterSerializer

from django_redis import get_redis_connection
from django.db.models import Q
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

# 连接redis
redis_conn = get_redis_connection('code')


# class CheckUsername(APIView):
#     """
#     检查用户名是否存在
#     """
#     @staticmethod
#     def get(request):
#         username = request.data.get('username')
#         is_exist = User.objects.filter(username=username).count()
#         return Response(data={'exists': is_exist}, status=status.HTTP_200_OK)
#
#
# class CheckMobile(APIView):
#     """
#     检查手机号是否已被绑定
#     """
#     @staticmethod
#     def get(request):
#         mobile = request.data.get('mobile')
#         is_exist = User.objects.filter(mobile=mobile).count()
#         return Response(data={'exists': is_exist}, status=status.HTTP_200_OK)


def check_sms_code(request):
    """
    验证短信验证码
    """
    mobile = request.data.get('mobile')
    sms_code = request.data.get('sms_code')
    correct = False
    if sms_code == redis_conn.get('{}_code'.format(mobile)).decode():
        correct = True
    return correct


def generate_token(user):
    """
    生成jwt_token
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


class SendSms(APIView):
    """
    发送短信验证码
    """
    @staticmethod
    def get(request, mobile):
        sms_code = '{:04d}'.format(random.randint(0, 9999))
        send_sms_code.delay(mobile, sms_code)
        redis_conn.set('{}_code'.format(mobile), sms_code, 60)
        return Response(
            data={
             'data': {'message': '信息已发送'},
             'code': 200
            },
            status=status.HTTP_200_OK
        )


class RegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        if check_sms_code(request):
            return super().create(request)
        return Response(
            data={
                'data': {'message': '短信验证码错误'},
                'code': 400
                },
            status=status.HTTP_400_BAD_REQUEST
        )


class SignInAPIView(APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(Q(username=username) | Q(mobile=username)).first()
        if not user:
            return Response(
                data={
                    'data': {'message': '用户不存在'},
                    'code': 200
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if password:
            if user.check_password(password):
                token = generate_token(user)
                return Response(
                    data={
                        'data': {'token': token, 'user_id': user.id},
                        'code': 200
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                data={
                    'data': {'message': '用户名或密码错误'},
                    'code': 200,
                },
                status=status.HTTP_400_BAD_REQUEST)
        if check_sms_code(request):
            token = generate_token(user)
            return Response(
                data={
                    'data': {'token': token, 'user_id': user.id},
                    'code': 200
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                'data': {'message': '验证码错误'},
                'code': 400
            },
            status=status.HTTP_400_BAD_REQUEST
        )
