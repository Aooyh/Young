import oss2
from django.core.files.storage import Storage


class AliFileStorage(Storage):
    """
    阿里云oss文件存储系统
    """
    def __init__(self, bucket):
        self.bucket_name = bucket
        self.region = 'oss-cn-hangzhou.aliyuncs.com'
        self.auth = oss2.Auth('LTAI4bC7jVIhaiNm', 'Eqc42Xv1hOcBZVaNhwtjHERQqW8qVh')
        self.bucket = oss2.Bucket(self.auth, 'http://{}'.format(self.region), self.bucket_name)

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        result = self.bucket.put_object(name, content)
        if result.status == 200:
            url = self.url(name)
            return url

    def save(self, name, content, max_length=None):
        if max_length is None:
            return self._save(name, content)

    def exists(self, name):
        exists = self.bucket.object_exists(name)
        if exists:
            return True
        return False

    def url(self, name):
        return 'http://{}.{}/{}'.format(self.bucket_name, self.region, name)
