from django.apps import AppConfig


class TradingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trading_app'

    def ready(self):
        import trading_app.signals
