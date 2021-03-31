"""
Django  3.1.4. settings for config project.
"""
import os
import sys

from pathlib import Path


from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Добавлен один уровень .parent для розделения settings.py
sys.path.append(str(BASE_DIR / 'apps'))  # Чтоб все приложения складывать в папку apps.


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default=0)))

# ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
# ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    # Local
    'accounts.apps.AccountsConfig',  # Кастомная админка.
    'base.apps.BaseConfig',  # Приложение для общего барахла.
    'blog.apps.BlogConfig',  # Блог.
    'travels.apps.TravelsConfig',  # Путешественник.
    'products.apps.ProductsConfig',  # Приложение с товарами.
    'orders.apps.OrdersConfig',  # Проложение для хранения корзыны и заказов.
    'crm.apps.CrmConfig',  # (CRM) Система управления взаимоотношениями с клиентами.
    'lms.apps.LmsConfig',  # (LMS) Система управления обучением.
    'scraping.apps.ScrapingConfig',  # Сервис для скрапинга вакансий по ЯП.

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'crispy_forms',  # Для обработки расширенных/пользовательских форм.
    'taggit',  # Подсистема тегов (удалить)
    'ckeditor',
    'ckeditor_uploader',
    'embed_video',  # Для видео.

    'rest_framework',  # Для REST API.
    # 'rest_framework_simplejwt',
    'djoser',  # For user registration and authentication endpoints
    'drf_yasg',  # Для автодокументации API.
    'corsheaders',  # Для  управления CORS.

    'debug_toolbar',
    'storages',  # Чтоб крутить статику и медиа на Amazon S3.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Для corsheaders.
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Для тулбара.
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Меняем пути для templates.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'orders.context_processors.cart',  # Для отображения контекста корзины.
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
#         'USER': os.environ.get('DB_USER', 'user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('POSTGRES_ENGINE', 'django.db.backends.sqlite3'),
#         'NAME': os.environ.get('POSTGRES_DB', BASE_DIR / 'db.sqlite3'),
#         'USER': os.environ.get('POSTGRES_USER', 'user'),
#         'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
#         'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
#         'PORT': os.environ.get('POSTGRES_PORT', '5432'),
#     }
# }
#
# import dj_database_url
# db = dj_database_url.config(conn_max_age=600, ssl_require=True)
# DATABASES['default'].update(db)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'db',  # set in docker-compose.yml
#         'PORT': 5432  # default postgres port
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / 'db.sqlite3'),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru'


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Переопределяем стандартную модель User.
AUTH_USER_MODEL = 'accounts.User'

# ________________________________________________________________
# Перенаправляем юзера после входа в аккаунт (по дефолту 'accounts/profile/').
LOGIN_REDIRECT_URL = 'home'
# Перенаправляем юзера после выхода с аккаунта.
LOGOUT_REDIRECT_URL = 'home'

# Кастомная авторизация
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Проверка на авторизацию через (username, password)
    'accounts.authentication.EmailAuthBackend',  # Проверка на авторизацию через (email, password)

    # 'social_core.backends.facebook.FacebookOAuth2',  # Аутентификация через facebook
    # 'social_core.backends.google.GoogleOAuth2',  # Аутентификация через Google
)


# Настройки email.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True

EMAIL_HOST = os.environ.get("EMAIL_HOST", None)
EMAIL_PORT = os.environ.get("EMAIL_PORT", None)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", None)


# Настройки для статики_______________________________________________
USE_AWS_S3 = bool(int(os.environ.get('USE_AWS_S3', default=0)))

if USE_AWS_S3:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', None)
    AWS_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
    AWS_DEFAULT_ACL = None
    AWS_S3_REGION_NAME = 'us-east-2'
    AWS_S3_SIGNATURE_VERSION = 's3v4'

    STATIC_URL = AWS_URL + '/static/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = AWS_URL + '/media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [BASE_DIR / 'static', ]
# ___________________________________________________________________


# Настройки для деплоя на heroku (staticfiles=False нужен для AWS_S3)
import django_heroku
django_heroku.settings(locals(), staticfiles=False)
