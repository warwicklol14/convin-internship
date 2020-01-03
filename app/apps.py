from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        # everytime server restarts
        import app.signals
