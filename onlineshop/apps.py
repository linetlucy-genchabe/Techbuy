from django.apps import AppConfig


class OnlineshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'onlineshop'
    
    def ready(self):
        import onlineshop.signals
