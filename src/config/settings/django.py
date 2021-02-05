"""
Django  3.1.4. settings for config project.
"""
import os
import sys
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv
load_dotenv()


# Django переменные.
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")
# PostgreSQL.
DB_NAME = os.getenv("DB_DATABASE"),
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
# Email.
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Добавлен один уровень .parent.
sys.path.append(str(BASE_DIR / 'apps'))  # Чтоб все приложения складывать в папку apps.


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG

ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    # Local
    'accounts.apps.AccountsConfig',  # Кастомная админка.
    'main.apps.MainConfig',  # Приложение для общего барахла.
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
    'whitenoise.runserver_nostatic',  # Чтоб крутить статику на деплое.
    'django.contrib.staticfiles',

    # Third-party
    'crispy_forms',  # Для обработки расширенных/пользовательских форм.
    'taggit',  # Подсистема тегов (удалить)
    'ckeditor',
    'ckeditor_uploader',
    'embed_video',  # Для видео.
    'rest_framework',  # Для REST API.
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Чтоб крутить статику на деплое.
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

db = dj_database_url.config()
DATABASES['default'].update(db)

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
# ________________________________________________________________


STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static', ]
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # new


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Настройки email для локальной розработки.
if DEBUG:  # Выводит сообщения в консоль
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = EMAIL_HOST
EMAIL_USE_TLS = True
EMAIL_PORT = EMAIL_PORT
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
