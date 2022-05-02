from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.recipes'

    def ready(self, *args, **kwargs) -> None:
        import apps.recipes.signals
        super_ready = super().ready(*args, **kwargs)
        return super_ready
