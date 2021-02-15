from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
     Определяет новый бэкэнд хранилища.
    """
    location = 'media'
    file_overwrite = False
