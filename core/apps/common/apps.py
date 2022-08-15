from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = "apps.common"

    def ready(self):
        import apps.common.signals  # noqa
