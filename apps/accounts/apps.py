from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'аккаунты'

    def ready(self):
        import accounts.signals
