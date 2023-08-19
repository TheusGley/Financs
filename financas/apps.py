from django.apps import AppConfig


class FinancasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'financas'
    def ready(self) :
        from financas import scheduler
        scheduler.start()
    