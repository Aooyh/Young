from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import status

from utils.ali_storage import AliFileStorage


class FileUploadAPIView(APIView):
    @staticmethod
    def post(request):
        # 创建存储bucket
        bucket = list(request.data.keys())[0]
        file = request.data.get(bucket)
        aliyun = AliFileStorage(bucket)

        # 生成图片编号
        user = request.user
        time_str = timezone.now().strftime('%d%H%M%S')
        image_name = '{}-{}-{}-{}'.format(user.username, bucket, time_str,  file.__str__())
        url = aliyun.save(image_name, file)
        if url:
            return Response(
                data={
                    'data': {'url': url},
                    'code': 200
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'data': {'message': '图片上传失败'},
                    'code': 400
                },
                status=status.HTTP_400_BAD_REQUEST
            )
