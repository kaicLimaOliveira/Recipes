from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authors'
    
    def ready(self, *args, **kwargs) -> None:
        import apps.authors.signals
        super_ready = super().ready(*args, **kwargs)
        return super_ready
