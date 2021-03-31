from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import HardSkill, SoftSkill, City


class User(AbstractUser):
    """
    Кастомизированая модель пользователя.
    Email зделано обязательным полем, username перейменовано для более корректного вывода на рус.
    Розширено новыми полями.
    """

    GENDER_MALE = 'GM'
    GENDER_FEMALE = 'GF'

    GENDER_CHOICES = [
        (GENDER_MALE, 'Мужской'),
        (GENDER_FEMALE, 'Женский'),
    ]

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'псевдоним',
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'))
    avatar = models.ImageField('аватар профиля', upload_to='user/avatar/', blank=True, null=True)
    mobile_phone = models.CharField('мобильный телефон', max_length=14, blank=True, null=True)
    bio = models.TextField('краткая биография', blank=True, null=True)
    github = models.CharField('ссылка на github', max_length=500, blank=True, null=True)
    birthday = models.DateField('дата рождения', blank=True, null=True)
    gender = models.CharField('ваш пол', max_length=2, choices=GENDER_CHOICES, default='GENDER_MALE')
    location = models.ForeignKey(
        City,
        related_name='users',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='локация'
    )
    hard_skill = models.ManyToManyField(
        HardSkill,
        related_name='users',
        blank=True,
    )
    soft_skill = models.ManyToManyField(
        SoftSkill,
        related_name='users',
        blank=True,
    )
    first_login = models.DateTimeField('время первого входа', blank=True, null=True)
    # Для работы app CRM.
    is_organisor = models.BooleanField(default=True, verbose_name='является ли главой организации crm')
    is_agent = models.BooleanField(default=False, verbose_name='является ли агентом crm')
    # Для работы рассылки вакансий app scraping.
    city = models.CharField('город', max_length=50, null=True, blank=True)
    language = models.ForeignKey('scraping.Language', on_delete=models.SET_NULL, null=True, blank=True)
    send_email = models.BooleanField('рассылка вакансий по email', default=False)
