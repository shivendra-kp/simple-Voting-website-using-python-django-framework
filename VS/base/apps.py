from django.apps import AppConfig
from backend.pubsub import PubSub
from backend.blockchain.blockchain import Blockchain



class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
    



