from django.apps import AppConfig

class RiskradarConfig(AppConfig):
    name = 'riskradar'

    def ready(self):
        import riskradar.signals
