from django.apps import AppConfig

from django.contrib.auth import get_user_model
from dotenv import load_dotenv, find_dotenv, set_key
import requests
import json
import os


class VertriebInterfaceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vertrieb_interface"

    # def ready(self):
    #     import vertrieb_interface.signals
    # def ready(self):
    #     from authentication.management.commands import update_user_angebots # Replace 'your_script' with the name of your Python script

    #     vertriebler_id = 26172000004347146
    #     command = update_user_angebots.Command()
    #     print(command.fetch_vertriebler_list_IDs(vertriebler_id))
