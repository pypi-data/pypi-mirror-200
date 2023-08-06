from django.apps import AppConfig


class BcmrConfig(AppConfig):
    name = 'bcmr'

    def ready(self):
        import bcmr.signals
