from django.apps import AppConfig


class AgreementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agreements'
    verbose_name: str = 'Convenios'

    def ready(self):
        from . import signals