from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Кастомизированая модель пользователя.
    Email зделано обязательным полем, username перейменовано для более корректного вывода на рус.
    Розширено новыми полями.
    """
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
    avatar = models.ImageField('аватарка', upload_to='user/avatar/', blank=True, null=True)

    # Для работы app CRM.
    is_organisor = models.BooleanField(default=True, verbose_name='является ли главой организации crm')
    is_agent = models.BooleanField(default=False, verbose_name='является ли агентом crm')
