from app.conf.environ import env

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='')
AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL', default='')
AWS_DEFAULT_ACL = env('AWS_DEFAULT_ACL', default='')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='')
